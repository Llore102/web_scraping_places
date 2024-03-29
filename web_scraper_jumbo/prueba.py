import time
import threading
import multiprocessing as mp
import requests
import bs4
  
def scrape_page(url):
    # Scrape the page and return the data
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    return soup.prettify()
  
class ThreadedScraper(threading.Thread):
    def __init__(self, urls):
        super().__init__()
        self.urls = urls
          
    def run(self):
        for url in self.urls:
            data = scrape_page(url)
            # Process the scraped data
  
def scrape_pages_mp(urls):
    with mp.Pool(2) as p:
        results = p.map(scrape_page, urls)
    return results
  
if __name__ == "__main__":
    # Test the multithreaded scraper
    urls = [
        "https://en.wikipedia.org/wiki/Main_Page",
        "https://www.google.com/"
    ]
  
    start = time.time()
      
    threads = []
    for i in range(2):
        t = ThreadedScraper(urls)
        threads.append(t)
        t.start()
      
    for t in threads:
        t.join()
          
    end = time.time()
    print(f"Time taken for multithreaded scraper: {end - start} seconds")
      
    # Test the multiprocessed scraper
    start = time.time()
    data = scrape_pages_mp(urls)
    end = time.time()
    print(f"Time taken for multiprocessed scraper: {end - start} seconds")