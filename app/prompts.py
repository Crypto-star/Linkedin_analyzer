"""
Prompt builder for LinkedIn profile analysis and job comparison.
"""

from typing import Optional
import re

def build_profile_analysis_prompt(profile_context: str, job_description: Optional[str], summary_context: Optional[str], user_intent: str) -> str:
    def extract_target_role(text: str) -> str:
        match = re.search(r"(?:become a|roadmap to|grow into|transition to(?:wards)?) (.+)", text.lower())
        return match.group(1).strip() if match else "the desired role"

    target_role = extract_target_role(user_intent)

    prompt = (
        "You are an expert AI career coach helping users grow professionally using real LinkedIn profile data.\n"
        "⚠️ Do NOT fabricate any details (like roles, degrees, or achievements).\n"
        "✅ Base all recommendations strictly on the user's real experience, skills, and learning history.\n"
        "🔁 Avoid repeating headings or content.\n"
        "🎯 Use insights from the profile's actual certifications, current or past roles, academic background, and any public society or project work.\n\n"
    )

    if summary_context:
        prompt += f"Conversation Summary:\n{summary_context}\n\n"

    prompt += f"User’s LinkedIn Profile:\n{profile_context}\n\n"

    if job_description:
        prompt += f"Job Description:\n{job_description}\n\n"

    # Dynamic intent routing
    if "roadmap" in user_intent or "become" in user_intent or "transition" in user_intent:
        prompt += (
            f"🎯 TASK: Build a personalized roadmap for the user to become a successful {target_role.title()}.\n"
            "Instructions:\n"
            "1. Start with a brief personalized overview of how their background (education, certifications, experience) aligns with this path.\n"
            "2. Identify specific skills, tools, or roles they are missing.\n"
            "3. Break the roadmap into Short (1–2 yrs), Medium (3–5 yrs), and Long-term (5–10 yrs) goals.\n"
            "4. Recommend only relevant learning resources (do not suggest what they already have).\n"
            "5. If applicable, relate current team or society roles to leadership development.\n"
        )

    elif "match" in user_intent or "fit" in user_intent:
        prompt += (
            "🎯 TASK: Assess the fit between the user's profile and the provided job description.\n"
            "Instructions:\n"
            "1. List key matched qualifications.\n"
            "2. Highlight any critical gaps.\n"
            "3. Provide a fit score (out of 100) and personalized improvement suggestions.\n"
        )

    elif "improve" in user_intent and "experience" in user_intent:
        prompt += (
            "🎯 TASK: Rewrite the user's work experience section to sound more professional and compelling.\n"
            "Instructions:\n"
            "- Use only real accomplishments from the profile.\n"
            "- Keep it brief, result-oriented, and quantifiable when possible.\n"
        )

    elif "what should i improve" in user_intent or "what do i need" in user_intent:
        prompt += (
            "🎯 TASK: Audit the profile to identify missing or weak areas.\n"
            "Instructions:\n"
            "Provide a markdown table:\n"
            "| Section | Present | Quality | Suggestions |\n"
            "|---------|---------|---------|-------------|\n"
        )

    else:
        prompt += (
            "🎯 TASK: Provide career guidance tailored to the user's current background and any goals implied.\n"
            "Instructions:\n"
            "- Suggest roles they might be well-suited for.\n"
            "- Recommend certifications, skills, or strategic pivots.\n"
            "- Make the advice specific and professional.\n"
        )

    return prompt
