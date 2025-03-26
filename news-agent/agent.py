from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.llms import HuggingFaceHub
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain import hub
from langchain.tools.retriever import create_retriever_tool




import os
from langchain.llms import HuggingFaceHub

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf token"

def get_toi_articles():
    url = "https://timesofindia.indiatimes.com/"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        if 'articleshow' in a_tag['href']:
            links.add("https://timesofindia.indiatimes.com" + a_tag['href'])
    
    return list(links)

def filter_articles_by_keywords(articles, keywords):
    filtered_articles = []
    for url in articles:
        try:
            article = Article(url)
            article.download()
            article.parse()
            text = article.text.lower()
            if any(keyword.lower() in text for keyword in keywords):
                filtered_articles.append({
                    "title": article.title,
                    "url": url,
                    "summary": article.text[:500]
                })
        except Exception:
            continue
    
    return filtered_articles

def fetch_news_by_keywords(keywords: str):
    keyword_list = keywords.split(",")
    articles = get_toi_articles()
    return filter_articles_by_keywords(articles, keyword_list)

news_tool = create_retriever_tool(
    fetch_news_by_keywords,
    "News Fetcher",
    "Fetch latest articles from Times of India based on provided keywords!",
)

prompt = hub.pull("hwchase17/openai-functions-agent")


llm = HuggingFaceHub(repo_id="meta-llama/Llama-3.2-3B-Instruct", model_kwargs={"temperature": 0.7, "max_length": 512})

agent = create_tool_calling_agent(llm, news_tool, prompt)

agent_executor = AgentExecutor(agent=agent, tools=news_tool, verbose=True)

print(agent_executor.invoke({"input": "Top 5 news on construction"}))


