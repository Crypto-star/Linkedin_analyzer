"""
Streamlit application for analyzing LinkedIn profiles using GPT with memory.
"""

# Main entry point for the Streamlit app.
# Handles UI inputs, profile scraping, job description input, and connects to the LangGraph for multi-step reasoning.

import streamlit as st
import os
from dotenv import load_dotenv

# Utility functions for scraping and greeting the user
from app.utils import scrape_linkedin_profile, get_user_greeting

# Chat and summarizer logic nodes
from app.nodes import chat_node, summarizer_node

# State machine library for chaining reasoning steps
from langgraph.graph import StateGraph, END

# Load environment variables from .env
load_dotenv()

# Set Streamlit app title and layout
st.set_page_config(page_title="LinkedIn Analyzer", layout="centered")
st.title("🔍 LinkedIn Analyzer with Memory")

# Initialize session state if not already done
if "state" not in st.session_state:
    st.session_state.state = {
        "messages": [],          # Chat history
        "profile": {},           # Scraped LinkedIn profile
        "job_description": "",   # Optional JD input
        "summary": "",           # Summary of chat
        "goal": ""               # User's latest query/intent
    }

# Input field for LinkedIn profile URL
url = st.text_input("🔗 Enter your LinkedIn Profile URL")
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

# Optional JD input
jd = st.text_area("💼 Optional: Paste Job Description")
if jd:
    st.session_state.state["job_description"] = jd

# Build a LangGraph with two reasoning steps: chat -> summarizer
builder = StateGraph(dict)
builder.add_node("chat", chat_node)
builder.add_node("summarizer", summarizer_node)
builder.set_entry_point("chat")
builder.add_edge("chat", "summarizer")
builder.add_edge("summarizer", END)
graph = builder.compile()

# Show chat history in UI
for msg in st.session_state.state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle user query input
user_input = st.chat_input("💬 Ask anything...")
if user_input:
    st.session_state.state["messages"].append({"role": "user", "content": user_input})
    st.session_state.state["goal"] = user_input
    result = graph.invoke(st.session_state.state)  # Invoke LangGraph reasoning
    st.session_state.state = result
    st.rerun()
