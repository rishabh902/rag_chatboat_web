import requests
from bs4 import BeautifulSoup


URLS = [
    "https://debales.ai/",
    "https://debales.ai/logistics",
    "https://debales.ai/blog",
    "https://debales.ai/case-studies",
    "https://debales.ai/ai-agent/multi-agent",
]

def scraper_debales():
    text_url=""
    print("Text is writting mode....")

    for url in URLS:
        print(f"Scarping {url}")
        response=requests.get(url,timeout=10)

        soup=BeautifulSoup(response.text, "html.parser")

        for tag in soup(["Script", "style"]):
            tag.decompose


        text=soup.get_text(separator=" ", strip=True).lower() #all text should be lowercase
        text_url= text_url + f"\n\nURL: {url}\n{text}" 

    #write text in text file 

    with open("data/dedebales_scraper.txt", "w", encoding="utf-8") as file:
        file.write(text_url)


    print("Scraper is complate . Data save successfully")

if __name__ == "__main__":
    scraper_debales()