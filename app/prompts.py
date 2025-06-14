"""
Prompt builder for LinkedIn profile analysis and job comparison.
"""

# Builds a system prompt for the AI assistant based on user intent.
# Adds contextual role-specific guidance, safety guardrails, and dynamic task selection.

from typing import Optional
import re

def build_profile_analysis_prompt(profile_context: str, job_description: Optional[str], summary_context: Optional[str], user_intent: str) -> str:
    def extract_target_role(text: str) -> str:
        match = re.search(r"(?:become a|roadmap to|grow into|transition to(?:wards)?) (.+)", text.lower())
        return match.group(1).strip() if match else "the desired role"

    target_role = extract_target_role(user_intent)

    # Header instructions
    prompt = (
        "You are an expert AI career coach helping users grow professionally using real LinkedIn profile data.\n"
        "⚠️ Do NOT fabricate any details.\n"
        "✅ Use only verified profile info.\n"
        "🔁 Avoid repetition.\n"
        "🎯 Base your guidance on actual skills, roles, education, certifications.\n\n"
    )

    if summary_context:
        prompt += f"Conversation Summary:\n{summary_context}\n\n"

    prompt += f"User’s LinkedIn Profile:\n{profile_context}\n\n"
    if job_description:
        prompt += f"Job Description:\n{job_description}\n\n"

    # Switch between task types based on intent
    if "roadmap" in user_intent or "become" in user_intent or "transition" in user_intent:
        prompt += (
            f"🎯 TASK: Build a roadmap to become a successful {target_role.title()}.\n"
            "Instructions: Tailor steps to their current experience and goals.\n"
        )
    elif "match" in user_intent or "fit" in user_intent:
        prompt += (
            "🎯 TASK: Compare the profile to the JD and rate their fit.\n"
        )
    elif "improve" in user_intent and "experience" in user_intent:
        prompt += (
            "🎯 TASK: Rewrite the experience section for clarity and impact.\n"
        )
    elif "what should i improve" in user_intent or "what do i need" in user_intent:
        prompt += (
            "🎯 TASK: Provide an audit table showing what can be improved.\n"
        )
    else:
        prompt += (
            "🎯 TASK: General career advice based on strengths and gaps.\n"
        )

    # Final safety guardrail to block non-career questions
    prompt += (
        "\n\n🔒 Final Guardrail:\n"
        "Only answer questions related to career, jobs, skills, resumes, and professional growth.\n"
        "If asked something else (health, dating, finance), politely decline and explain your scope."
    )

    return prompt
