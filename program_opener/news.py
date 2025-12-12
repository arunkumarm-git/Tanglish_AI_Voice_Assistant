import os
import requests
from dotenv import load_dotenv

def get_news(topic: str):
    load_dotenv()
    """
    Fetches and formats the top 3 news headlines for a given topic.
    """
    API_KEY = os.getenv("NEWS_API_KEY")
    # Use the 'everything' endpoint to search by topic (q=topic)
    url = f'https://newsapi.org/v2/everything?qInTitle={topic}&apiKey={API_KEY}&language=en&sortBy=publishedAt'
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        
        news_data = response.json()
        articles = news_data.get("articles", [])

        if not articles:
            return f"Sorry, I couldn't find any recent news headlines about {topic}."

        # Format the top 3 headlines into a single, clean string
        headlines = [f"{i+1}. {article['title']}" for i, article in enumerate(articles[:3])]
        formatted_news = f"Here are the top headlines on {topic}: {' '.join(headlines)}"
        
        return formatted_news

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to News API: {e}")
        return "Sorry, I'm having trouble connecting to the news service right now."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred while fetching the news."