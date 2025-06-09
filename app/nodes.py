"""
LangGraph nodes to handle chat interactions and memory summarization.
"""

from app.prompts import build_profile_analysis_prompt
from app.utils import get_profile_summary
from langchain_openai import ChatOpenAI

def chat_node(state: dict) -> dict:
    """
    Chat node that generates GPT responses based on profile, job description, and chat history.

    Args:
        state (dict): The current session state.

    Returns:
        dict: Updated session state with new assistant message.
    """
    profile = state.get("profile", {})
    messages = state.get("messages", [])
    jd = state.get("job_description", "")
    summary = state.get("summary", "")

    llm = ChatOpenAI(model_name="gpt-4o-mini")
    
    # Build context-aware prompt for GPT
    prompt = build_profile_analysis_prompt(
        profile_summary=get_profile_summary(profile),
        job_description=jd,
        summary_context=summary
    )

    # Add latest messages (last 6) for conversation continuity
    chat_history = [{"role": "system", "content": prompt}] + messages[-6:]
    response = llm.invoke(chat_history)

    messages.append({"role": "assistant", "content": response.content})
    return {
        "messages": messages,
        "profile": profile,
        "job_description": jd,
        "summary": summary
    }

def summarizer_node(state: dict) -> dict:
    """
    Summarizer node that compresses conversation history into a summary for context retention.

    Args:
        state (dict): The current session state.

    Returns:
        dict: Updated session state with summary field added.
    """
    
    llm = ChatOpenAI(model_name="gpt-4o-mini")
    messages = state.get("messages", [])

    
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages]) # Convert chat history to text format
    
   
    summary_prompt = f"Summarize this chat to preserve user intent and context:\n\n{history_text}" # Build summary prompt
    
    
    summary = llm.invoke([{"role": "user", "content": summary_prompt}]).content # Invoke LLM to generate summary
    
    state["summary"] = summary
    return state
