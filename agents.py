import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url

load_dotenv()

llm = init_chat_model(
    model="mistral-small",
    model_provider="mistralai",
    api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0,
)


def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )


def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Produce highly professional AI research reports with clear structure, executive summaries, and actionable recommendations."),
    ("human", """Write an advanced research report on the topic below using the gathered research.

Topic: {topic}

Research Gathered:
{research}

Please include the following sections in your response:
- Executive Summary: one paragraph that highlights the main conclusion.
- Methodology: explain how the research was synthesized and what data sources were used.
- Key Findings: list at least 4 strong insights with supporting detail.
- Implications: describe what the findings mean for strategy or decision-making.
- Recommended Actions: provide 3 concrete next steps or recommendations.
- Sources: list the URLs, references, or evidence used.

Use markdown formatting, headings, numbered lists, and bullet points. Keep the tone professional, concise, and research-focused."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# critic_chain

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Evaluate the report for accuracy, clarity, relevance, and actionability."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Opportunities to Improve:
- ...
- ...

Missing Evidence or Risks:
- ...
- ...

One-line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser() 