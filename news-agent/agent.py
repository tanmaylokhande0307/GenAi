from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.llms import HuggingFaceHub
import requests
from bs4 import BeautifulSoup
from newspaper import Article

import os
from langchain.llms import HuggingFaceHub

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "your_huggingface_api_token"

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

news_tool = Tool(
    name="News Fetcher",
    func=fetch_news_by_keywords,
    description="Fetch latest articles from Times of India based on provided keywords"
)

llm = HuggingFaceHub(repo_id="deepseek-ai/deepseek-llm-7b-chat", model_kwargs={"temperature": 0.7, "max_length": 512})

agent = initialize_agent(
    tools=[news_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

def main():
    query = "technology, finance, politics"  # Modify keywords as needed
    response = agent.run(query)
    print(response)

if __name__ == "__main__":
    main()
