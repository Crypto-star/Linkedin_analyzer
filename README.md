
# 🔍 LinkedIn Analyzer

An AI-powered Streamlit application that analyzes LinkedIn profiles, compares them with job descriptions, suggests improvements, and provides career guidance using GPT and LangGraph with memory.

> 🌐 **Live App**: [https://your-deployed-url.streamlit.app](https://your-deployed-url.streamlit.app)

---

## 🚀 Features

✅ **LinkedIn Profile Scraping**

✅ **Job Fit Analysis & Match Score**

✅ **Career Suggestions & Skill Gap Identification**

✅ **GPT-4o with Conversational Memory**

✅ **Smart Summarization for Long Chats**

✅ **Prompt Guardrails Against Irrelevant Queries**

---

## 📦 Tech Stack

* **Frontend**: [Streamlit](https://streamlit.io/)
* **LLM**: OpenAI `gpt-4o-mini`
* **Memory & Flow**: [LangGraph](https://github.com/langchain-ai/langgraph)
* **Scraper**: [Apify LinkedIn Scraper](https://apify.com/supreme_coder/linkedin-profile-scraper)
* **Backend**: Python 3.10+

---

## 🧠 How It Works

1. **User inputs a LinkedIn profile URL**
2. **Profile is scraped using Apify (once per session)**
3. **Optional: Add a job description to evaluate job fit**
4. **LangGraph routes the chat via `chat_node` and `summarizer_node`**
5. **GPT returns suggestions, analysis, and continues a memory-aware conversation**

---

## 🗂️ Project Structure

```
linkedin-analyzer/
├── app/
│   ├── main.py             # Streamlit UI logic
│   ├── utils.py            # Scraper + profile formatter
│   ├── prompts.py          # GPT prompt builder
│   ├── nodes.py            # LangGraph nodes (chat, summarizer)
│   └── __init__.py
├── .env.example            # Example environment variables
├── requirements.txt        # Python dependencies
├── README.md               # You're reading it
```

---

## ⚙️ Setup Instructions

### 🔧 1. Clone the Repository

```bash
git clone https://github.com/your-username/linkedin-analyzer.git
cd linkedin-analyzer
```

### 🔐 2. Set Environment Variables

Create a `.env` file or use `.streamlit/secrets.toml` for Streamlit Cloud:

#### Locally (`.env`):

```env
OPENAI_API_KEY=your-openai-key
APIFY_TOKEN=your-apify-token
```

#### Streamlit Cloud (`.streamlit/secrets.toml`):

```toml
OPENAI_API_KEY = "your-openai-key"
APIFY_TOKEN = "your-apify-token"
```

### 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### ▶️ 4. Run the App

```bash
streamlit run app/main.py
```

Visit [http://localhost:8501](http://localhost:8501) to use the app locally.

---

## 🌐 Deployment (Streamlit Cloud)

1. Push your code to GitHub
2. Visit [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub repo
4. Add `OPENAI_API_KEY` and `APIFY_TOKEN` in app secrets
5. Click **Deploy**

You’ll get a public URL like:

```
https://linkedin-analyzer.streamlit.app
```

---

## 🧪 Example Usage

* **Enter a LinkedIn URL** to fetch profile insights
* **Paste a job description** to check how well the profile matches
* **Ask questions like**:

  * *“How can I improve my LinkedIn profile?”*
  * *“What skills should I add for this job?”*
  * *“Suggest certifications I can pursue”*

---

## 🚧 Guardrails

This AI assistant only responds to topics related to:

* LinkedIn Profiles
* Job Descriptions
* Career Growth & Skill Gaps

❌ It politely refuses to answer off-topic questions (e.g., politics, general trivia).

---

## 🙋 Author

**Harshvardhan Sharma**
Built with ❤️ using LangGraph + Streamlit + GPT.
Feel free to reach out for collaboration or hiring.
