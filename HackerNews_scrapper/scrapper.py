from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError, Timeout, RequestException
import time
import os

def scrape(num_pages):

    for page in range(1, num_pages + 1):
        url = f"https://news.ycombinator.com/?p={page}"
        print(f"--- Scraping Page {page}")

        try:
            response = requests.get(url, timeout=5)
            # Triggers an HTTPError if status is 4xx or 5xx
            response.raise_for_status()
            print("Success! Data retrieved.")
            soup = BeautifulSoup(response.text, "lxml")
            # fill in anything missing with default values
            article_list = []
            rows = soup.find_all("tr", class_="athing submission")
            
            for row in rows:
                article_num = row.find("span", class_="rank").text[:-1]
                title_line = row.find("span", class_="titleline")

                title = title_line.find("a").text if title_line else "N/A"
                url = title_line.find("a")["href"] if title_line else "N/A"
                website_tag = title_line.find("span", class_="sitestr") if title_line else None
                website = website_tag.text if website_tag else "N/A"

                # gets next <tr> after current one
                subtext_row = row.find_next_sibling("tr")

                score = 0
                author = "N/A"
                time_posted = "N/A"

                if subtext_row:
                    score_tag = subtext_row.find("span", class_="score")
                    author_tag = subtext_row.find("a", class_="hnuser")
                    age_tag = subtext_row.find("span", class_="age")
                    if score_tag:
                        score = score_tag.text
                    if author_tag:
                        author = author_tag.text
                    if age_tag:
                        time_posted = age_tag.a.text
                
                article = {
                    "Article Number": article_num,
                    "Article Title": title,
                    "Source Website": website,
                    "Source URL": url,
                    "Article Author": author,
                    "Article Score": score,
                    "Posted": time_posted
                }
                article_list.append(article)
            write_page_to_file(page, article_list)

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

    print(f"Finished scraping. Wrote to {num_pages} files.")    
    return

def write_page_to_file(page, article_list):
    target_dir = "HackerNews"
    os.makedirs(target_dir, exist_ok=True)

    file_name = f"NewsPage{page}.txt"
    file_path = os.path.join(target_dir, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("-" *  30 + "\n")
        f.write(f"Page {page}")
        f.write("-" *  30 + "\n\n")
        for article in article_list:
            f.write(f"Article Number: {article["Article Number"]}\n")
            f.write(f"Article Title: {article["Article Title"]}\n")
            f.write(f"Source Website: {article["Source Website"]}\n")
            f.write(f"Source URL: {article["Source URL"]}\n")
            f.write(f"Article Author: {article["Article Author"]}\n")
            f.write(f"Article Score: {article["Article Score"]}\n")
            f.write(f"Posted: {article["Posted"]}\n")
            f.write("-" * 30 + "\n\n")
        print(f"Successfully saved {file_name} to {target_dir}/")

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