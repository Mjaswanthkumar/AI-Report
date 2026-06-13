import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def summarize(articles):

    content = ""

    for article in articles:
        content += f"""
Title: {article['title']}
Summary: {article['summary']}
"""

    prompt = f"""
You are an expert AI intelligence analyst.

Your job is to convert raw AI news articles into a highly compressed, high-signal “AI Daily Intelligence Brief”.

You are NOT a summarizer. You are an intelligence filter.

----------------------------
INPUT:
A list of AI news articles (title, short summary, link).

----------------------------
TASK:
From the input, extract ONLY high-impact information and structure it into insights.

Focus only on:

1. NEW LLM MODELS
- Any new model release (GPT, Claude, Gemini, Llama, Qwen, DeepSeek, etc.)
- Improvements in existing models
- Benchmark breakthroughs

2. AI INNOVATIONS
- New AI capabilities
- Agent systems
- Tool use / MCP / workflows
- Architecture changes

3. NEW DISCOVERIES / RESEARCH
- Important papers
- Scientific breakthroughs
- Training techniques
- Reasoning / memory / planning improvements

4. BIG COMPANY MOVES
- OpenAI, Google, Anthropic, Meta, Microsoft, Amazon
- Acquisitions, partnerships, funding
- Product launches

5. OPEN SOURCE + DEVELOPER ECOSYSTEM
- New frameworks
- GitHub AI projects
- Developer tools (LangGraph, CrewAI, Hugging Face, etc.)

6. INDUSTRY SIGNALS
- Market trends
- Regulation changes
- Enterprise adoption patterns

7. ACTIONABLE INSIGHTS
- What the user should BUILD today
- What to EXPLORE
- What to WATCH

----------------------------
OUTPUT RULES (VERY IMPORTANT):

- Keep output extremely concise
- Remove duplication
- Merge similar news items
- Do NOT include unnecessary explanation
- Use bullet points only
- No long paragraphs
- Prioritize signal over completeness

----------------------------
TELEGRAM LIMIT RULE:

The FINAL output MUST NOT exceed 3800 characters.

This is mandatory.

If content is too large:
- remove low priority items
- compress sentences
- merge similar updates
- keep only top 3–5 items per category

Never exceed 3800 characters under any condition.

----------------------------
FORMAT:

🚀 AI DAILY INTELLIGENCE BRIEF

1. NEW LLM MODELS
- ...

2. AI INNOVATIONS
- ...

3. RESEARCH BREAKTHROUGHS
- ...

4. BIG COMPANY MOVES
- ...

5. OPEN SOURCE / DEV TOOLS
- ...

6. INDUSTRY SIGNALS
- ...

7. ACTIONABLE INSIGHTS
- Build:
- Explore:
- Watch:

----------------------------
FINAL PRINCIPLE:

Think like a top-tier AI analyst writing for a builder who wants only:
- what changed
- why it matters
- what to do next

{content}

if articles are none, give no articles exist in the input.
"""

    response = model.generate_content(prompt)

    return response.text