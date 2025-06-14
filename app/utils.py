"""
Utility functions for scraping LinkedIn profiles and processing data.
"""

# Utility functions: scrape LinkedIn profile, greet user, and extract structured profile info.

from apify_client import ApifyClient
from typing import Dict, Any
import json
import os

# Save all scraped profiles for logging/debugging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_json(filename: str, data: Any):
    with open(os.path.join(LOG_DIR, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Scrape a LinkedIn profile using Apify actor
def scrape_linkedin_profile(token: str, url: str) -> Dict[str, Any]:
    try:
        if not url or not url.startswith("https://www.linkedin.com/in/"):
            raise ValueError("Please provide a valid LinkedIn profile URL.")
        client = ApifyClient(token)
        run_input = {
            "findContacts": False,
            "scrapeCompany": False,
            "urls": [{"url": url, "method": "GET"}]
        }
        run = client.actor("supreme_coder/linkedin-profile-scraper").call(run_input=run_input)
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        profile = items[0] if items else {}
        log_json("scraped_profile.json", profile)
        return profile
    except Exception as e:
        print(f"Error scraping LinkedIn profile: {e}")
        return {}

# Generate greeting from scraped profile
def get_user_greeting(profile: dict) -> str:
    name = f"{profile.get('firstName', '')} {profile.get('lastName', '')}".strip()
    if not name:
        name = profile.get("fullName", "there")
    headline = profile.get("headline") or profile.get("occupation") or "a professional"
    return f"Hi {name}! 👋 I see you're working as {headline}. How can I help you today?"

# Turn raw profile JSON into structured readable string for LLM
def get_detailed_profile_context(profile: dict) -> str:
    fields = [
        ("Full Name", "fullName"),
        ("First Name", "firstName"),
        ("Last Name", "lastName"),
        ("Headline", "headline"),
        ("Summary", "summary"),
        ("Location", "geoLocationName"),
        ("Occupation", "occupation"),
        ("Job Title", "jobTitle"),
        ("Company Name", "companyName"),
        ("Industry", "industryName"),
        ("Connections", "connectionsCount"),
        ("Followers", "followersCount"),
        ("Skills", "skills"),
        ("Certifications", "certifications"),
        ("Languages", "languages"),
        ("Courses", "courses"),
        ("Honors", "honors"),
        ("Volunteer Experience", "volunteerExperiences"),
        ("Experience", "positions"),
        ("Education", "educations")
    ]
    context = ""
    for label, key in fields:
        value = profile.get(key)
        if not value:
            context += f"{label}: [Not Provided]\n"
        elif isinstance(value, list):
            context += f"{label}:\n"
            for item in value:
                context += f"- {json.dumps(item, ensure_ascii=False)}\n"
        else:
            context += f"{label}: {value}\n"
    return context
