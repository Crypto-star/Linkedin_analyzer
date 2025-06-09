"""
Prompt builder for LinkedIn profile analysis and job comparison.
"""

from typing import Optional

def build_profile_analysis_prompt(profile_summary: str, job_description: Optional[str] = None, summary_context: Optional[str] = None) -> str:
    """
    Constructs a prompt for the GPT model based on LinkedIn profile and job description.

    Args:
        profile_summary (str): Text summary of the LinkedIn profile.
        job_description (Optional[str]): Job description for comparison (optional).
        summary_context (Optional[str]): Summarized conversation history (optional).

    Returns:
        str: Full prompt string for the model.
    """
    
    prompt = (
        "You are a professional career assistant helping users optimize their LinkedIn profiles, improve job fit, "
        "and receive personalized career advice.\n\n"
        "⚠️ Only respond to questions related to:\n"
        "- LinkedIn profiles\n"
        "- Job descriptions\n"
        "- Skill gaps\n"
        "- Career planning and development\n\n"
        "❌ If the user asks something outside of this domain (e.g., general trivia, politics, history), politely decline and explain that you only focus on career-related topics.\n\n"
    )

    if summary_context:
        prompt += f"Conversation so far (summary):\n{summary_context}\n\n"

    prompt += f"User's LinkedIn profile:\n{profile_summary}\n\n"

    if job_description:
        prompt += f"Target job description:\n{job_description}\n\n"
        prompt += "Compare the profile against the job description and provide fit analysis, match score, and improvement tips.\n"
    else:
        prompt += "Provide general improvement suggestions based on the profile."

    return prompt
