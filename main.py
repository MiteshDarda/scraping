from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import time


class EFloraOfIndiaScraper:
    def __init__(self, base_url="https://efloraofindia.com/"):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        self.session = requests.Session()
        self.visited = set() # To keep track of visited URLs
    
    def get_html(self, url):
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text
    
    def scrape(self, url=None, depth=1):
        if depth < 1: return
        if url is None:
            url = self.base_url
        if url in self.visited:
            return
        self.visited.add(url)
        
        print("---------------------------------------------------------------------------------------")
        print(f"Scraping {url} at depth {depth}")
        print("---------------------------------------------------------------------------------------")
        print()
        print()
        
        html = self.get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        
        unordered_lists = soup.find_all("ul")
        
        #https://efloraofindia.com/
        #https://efloraofindia.com/article-categories
        for i, ul in enumerate(unordered_lists):
            li = ul.find_all("li")
            print("====================================")
            print(i)
            print("====================================")
            for item in li:
                print("====================================")
                print(item.text)
                print("====================================")
                print()
                scraped_url = item.find("a")
                if scraped_url:
                    full_url = scraped_url.get("href")
                    print("Full URL ::> ",full_url)
                    print()
                    # time.sleep(1)  # Add a delay of 0.01 second
                    time.sleep(0.01)
                    self.scrape(full_url, depth-1)
                print("====================================")
                print()
            print("====================================")
            print("====================================")
            print("====================================")
            print()
        
        


if __name__ == "__main__":
    scraper = EFloraOfIndiaScraper()
    scraper.scrape(depth=1)
