"""
Streamlit application for analyzing LinkedIn profiles using GPT with memory.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from app.utils import scrape_linkedin_profile, get_user_greeting
from app.nodes import chat_node, summarizer_node
from langgraph.graph import StateGraph, END

load_dotenv() # Load environment variables (API keys)

# Configure Streamlit page settings
st.set_page_config(page_title="LinkedIn Analyzer", layout="centered") 
st.title("🔍 LinkedIn Analyzer with Memory")

# Initialize session state if not exists
if "state" not in st.session_state:
    st.session_state.state = {
        "messages": [],
        "profile": {},
        "job_description": "",
        "summary": ""
    }

url = st.text_input("🔗 Enter your LinkedIn Profile URL") # Text input for LinkedIn profile URL


# Trigger profile scraping if URL is provided and no profile data is stored yet
if url and not st.session_state.state["profile"]:
    token = os.getenv("APIFY_TOKEN")
    with st.spinner("Scraping profile..."):
        profile = scrape_linkedin_profile(token, url)
        if profile:
            st.session_state.state["profile"] = profile
            greeting = get_user_greeting(profile)
            st.session_state.state["messages"].append({"role": "assistant", "content": greeting})
            st.success("Profile fetched successfully.")
            st.rerun()
        else:
            st.error("Unable to fetch profile.")

# Optional text area to paste a job description
jd = st.text_area("💼 Optional: Paste Job Description")
if jd:
    st.session_state.state["job_description"] = jd

# Build LangGraph to handle chat and summarization
builder = StateGraph(dict)
builder.add_node("chat", chat_node)
builder.add_node("summarizer", summarizer_node)
builder.set_entry_point("chat")
builder.add_edge("chat", "summarizer")
builder.add_edge("summarizer", END)
graph = builder.compile()

# Display past chat messages
for msg in st.session_state.state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Capture user input and invoke LangGraph pipeline
user_input = st.chat_input("💬 Ask anything...")
if user_input:
    st.session_state.state["messages"].append({"role": "user", "content": user_input})
    result = graph.invoke(st.session_state.state)
    st.session_state.state = result
    st.rerun()
