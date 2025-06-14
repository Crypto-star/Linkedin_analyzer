"""
LangGraph nodes to handle chat interactions and memory summarization.
"""

# Chat and summarizer nodes used in LangGraph.
# These act as modular reasoning steps based on user profile, intent, and JD.

from app.prompts import build_profile_analysis_prompt
from app.utils import get_detailed_profile_context
from langchain_openai import ChatOpenAI

# Extract user's last intent from the latest chat message
def detect_user_intent(messages: list) -> str:
    if not messages:
        return "general"
    return messages[-1]["content"].lower()

# Main reasoning step: generate a response based on profile, JD, and intent
def chat_node(state: dict) -> dict:
    profile = state.get("profile", {})
    messages = state.get("messages", [])
    jd = state.get("job_description", "")
    summary = state.get("summary", "")
    user_intent = detect_user_intent(messages)

    llm = ChatOpenAI(model_name="gpt-4o")  # Use OpenAI GPT-4o

    # Build prompt based on intent
    prompt = build_profile_analysis_prompt(
        profile_context=get_detailed_profile_context(profile),
        job_description=jd,
        summary_context=summary,
        user_intent=user_intent
    )

    chat_history = [{"role": "system", "content": prompt}] + messages[-6:]  # Append recent history
    response = llm.invoke(chat_history)

    messages.append({"role": "assistant", "content": response.content})
    return {
        "messages": messages,
        "profile": profile,
        "job_description": jd,
        "summary": summary
    }

# Secondary reasoning step: summarize the chat for context persistence
def summarizer_node(state: dict) -> dict:
    llm = ChatOpenAI(model_name="gpt-4o")
    messages = state.get("messages", [])
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    summary_prompt = f"Summarize this chat to preserve user intent and context:\n\n{history_text}"
    summary = llm.invoke([{"role": "user", "content": summary_prompt}]).content
    state["summary"] = summary
    return state
