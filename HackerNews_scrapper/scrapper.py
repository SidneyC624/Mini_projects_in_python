from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError, Timeout, RequestException
import time

def scrape(num_pages):
    all_stories = []
    
    for page in range(1, num_pages + 1):
        url = f"https://news.ycombinator.com/?p={page}"
        print(f"--- Scraping Page {page}")

        try:
            response = requests.get(url, timeout=5)
            # Triggers an HTTPError if status is 4xx or 5xx
            response.raise_for_status()
            print("Success! Data retrieved.")
            soup = BeautifulSoup(response.text, "lxml")
            stories = soup.find_all("span", class_ = "titleline")

            for story in stories:
                title = story.get_text()
                link = story.find("a")["href"]
                all_stories.append({"title": title, "link": link})
        
        except Timeout:
            print("Error: The request timed out. Check your internet of the server status.")
        
        except HTTPError as err:
            if response.status_code == 404:
                print("Error: 404 Page Not Found. The URL might be wrong.")
            else:
                print(f"HTTP Error occurred: {err}")

        except RequestException as err:
            print(f"An unexpected error occured: {err}")
        # to prevent hitting the server too fast
        time.sleep(1)

    print(f"Gathered {len(all_stories)} stories")
    return

if __name__ == "__main__":
    MAX_PAGES = 20
    while True:
        num_pages = input(f"Enter the number of pages that you want to scrape max({MAX_PAGES}): ")

        if not num_pages.isdigit():
            print("Please input a valid integer.")
            continue

        num_pages_int =  int(num_pages)
        if num_pages_int > MAX_PAGES:
            print(f"You are not allowed to scrape more than {MAX_PAGES} pages.")
        elif num_pages_int < 0:
            print("Please input a positive integer.")
        else:
            print(f"Success! Preparing to scrape {num_pages_int} pages.")
            break
    scrape(num_pages_int)