"""
Utility functions for scraping LinkedIn profiles and processing data.
"""

from apify_client import ApifyClient
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

def scrape_linkedin_profile(apify_token: str, url: str) -> Optional[Dict[str, Any]]:
    """
    Scrapes a LinkedIn profile using the Apify API.

    Args:
        apify_token (str): APIFY API token.
        url (str): LinkedIn profile URL.

    Returns:
        dict | None: Profile data dictionary or None if scraping fails.
    """
    try:
        client = ApifyClient(apify_token)
        run_input = {"urls": [{"url": url}], "findContacts": False}
        run = client.actor("supreme_coder/linkedin-profile-scraper").call(run_input=run_input)
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            return item
    except Exception as e:
        logger.error(f"Scraping error: {e}")
        return None

def get_user_greeting(profile: Dict[str, Any]) -> str:
    """
    Generates a greeting message based on the user's name in the profile.

    Args:
        profile (dict): LinkedIn profile data.

    Returns:
        str: Personalized greeting string.
    """
    name = profile.get("firstName", profile.get("name", "there"))
    return f"Hi {name}! How can I help you improve your career today?"

def get_profile_summary(profile: Dict[str, Any]) -> str:
    """
    Builds a readable summary of the LinkedIn profile for use in prompts.

    Args:
        profile (dict): LinkedIn profile data.

    Returns:
        str: Formatted profile summary string.
    """
    lines = []
    lines.append(f"Name: {profile.get('firstName', '')} {profile.get('lastName', '')}")
    lines.append(f"Headline: {profile.get('headline', '')}")
    lines.append(f"Summary: {profile.get('summary', '')}")
    lines.append(f"Location: {profile.get('geoLocationName', '')}, {profile.get('geoCountryName', '')}")
    lines.append(f"Industry: {profile.get('industryName', '')}")
    lines.append(f"Followers: {profile.get('followersCount', 'N/A')}, Connections: {profile.get('connectionsCount', 'N/A')}")
    
    # Format work experience
    positions = profile.get("positions", [])
    if positions:
        lines.append("Experience:")
        for pos in positions:
            title = pos.get("title", "")
            company = pos.get("companyName", "")
            loc = pos.get("locationName", "")
            start = pos.get("timePeriod", {}).get("startDate", {})
            end = pos.get("timePeriod", {}).get("endDate", {})
            start_str = f"{start.get('month', '')}/{start.get('year', '')}" if start else ""
            end_str = f"{end.get('month', '')}/{end.get('year', '')}" if end else "Present"
            lines.append(f" - {title} at {company} ({loc}) [{start_str} - {end_str}]")

    # Format education
    educations = profile.get("educations", [])
    if educations:
        lines.append("Education:")
        for edu in educations:
            degree = edu.get("degreeName", "")
            field = edu.get("fieldOfStudy", "")
            school = edu.get("schoolName", "")
            start = edu.get("timePeriod", {}).get("startDate", {}).get("year", "")
            end = edu.get("timePeriod", {}).get("endDate", {}).get("year", "")
            lines.append(f" - {degree} in {field} at {school} [{start} - {end}]")

    # Format certifications
    certs = {cert.get("name"): cert for cert in profile.get("certifications", [])}
    if certs:
        lines.append("Certifications:")
        for name, cert in certs.items():
            authority = cert.get("authority", "")
            start = cert.get("timePeriod", {}).get("startDate", {})
            start_str = f"{start.get('month', '')}/{start.get('year', '')}" if start else ""
            lines.append(f" - {name} by {authority} [{start_str}]")

    # Format skills
    skills = profile.get("skills", [])
    if skills:
        lines.append("Skills: " + ", ".join(skills))

    return "\n".join([line for line in lines if line.strip()])
