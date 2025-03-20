from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import time
import csv
import os


class EFloraOfIndiaScraper:
    def __init__(self, base_url="https://efloraofindia.com/"):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        self.session = requests.Session()
        self.visited = set()  # To keep track of visited URLs
        self.urls_by_depth = {}  # Dictionary to store URLs by depth
    
    def get_html(self, url):
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text
    
    def save_to_txt(self, filename="scraped_urls.txt"):
        """Save the URLs to a text file, organized by depth."""
        with open(filename, 'w', encoding='utf-8') as f:
            for depth in sorted(self.urls_by_depth.keys()):
                f.write(f"Depth {depth}:\n")
                f.write("-" * 80 + "\n")
                for url in self.urls_by_depth[depth]:
                    f.write(f"{url}\n")
                f.write("\n\n")
        print(f"URLs saved to {filename}")
    
    def save_to_csv(self, filename="scraped_urls.csv"):
        """Save the URLs to a CSV file with depth information."""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Depth", "URL", "Title"])
            
            for depth in sorted(self.urls_by_depth.keys()):
                for url_info in self.urls_by_depth[depth]:
                    if isinstance(url_info, tuple) and len(url_info) == 2:
                        url, title = url_info
                        writer.writerow([depth, url, title])
                    else:
                        writer.writerow([depth, url_info, ""])
        print(f"URLs saved to {filename}")
    
    def scrape(self, depth_urls=None, current_depth=0, output_format="both"):
        """
        Scrape the website based on depth_urls.
        
        Args:
            depth_urls: List of URL prefixes for each depth level
            current_depth: Current depth level being processed
            output_format: Format to save results ('txt', 'csv', or 'both')
        """
        if depth_urls is None:
            depth_urls = [self.base_url]
        
        # Clear previous data
        self.urls_by_depth = {}
        self.visited = set()
        
        # Start processing from the first URL
        if current_depth == 0:
            self._process_url(depth_urls[0], depth_urls, current_depth)
            
            # Save the results
            if output_format.lower() in ['txt', 'both']:
                self.save_to_txt()
            if output_format.lower() in ['csv', 'both']:
                self.save_to_csv()
    
    def _process_url(self, url, depth_urls, current_depth):
        """
        Process a single URL and its links.
        
        Args:
            url: URL to process
            depth_urls: List of URL prefixes
            current_depth: Current depth level
        """
        if url in self.visited:
            return
        
        self.visited.add(url)
        
        # Initialize the list for this depth if not exists
        if current_depth not in self.urls_by_depth:
            self.urls_by_depth[current_depth] = []
        
        print("---------------------------------------------------------------------------------------")
        print(f"Scraping {url} at depth {current_depth}")
        print("---------------------------------------------------------------------------------------")
        print()
        print()
        
        try:
            html = self.get_html(url)
            soup = BeautifulSoup(html, "html.parser")
            
            # Get page title if available
            title = soup.title.string if soup.title else ""
            
            # Save URL with title
            self.urls_by_depth[current_depth].append((url, title.strip() if title else ""))
            
            unordered_lists = soup.find_all("ul")
            
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
                        link_text = scraped_url.text.strip()
                        print("Full URL ::> ", full_url)
                        print()
                        
                        # Only process URLs that match the prefix for the next depth
                        if current_depth + 1 < len(depth_urls):
                            next_prefix = depth_urls[current_depth + 1]
                            if full_url and full_url.startswith(next_prefix):
                                time.sleep(0.01)  # Add a delay of 0.01 second
                                self._process_url(full_url, depth_urls, current_depth + 1)
                    print("====================================")
                    print()
                print("====================================")
                print("====================================")
                print("====================================")
                print()
        except Exception as e:
            print(f"Error processing {url}: {e}")


if __name__ == "__main__":
    scraper = EFloraOfIndiaScraper()
    # Example usage with depth_urls
    depth_urls = [
        "https://efloraofindia.com/",
        "https://efloraofindia.com/article-categories",
        "https://efloraofindia.com/efi"
    ]
    # Save to both txt and csv files
    scraper.scrape(depth_urls=depth_urls, output_format="both")