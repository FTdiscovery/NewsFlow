import requests
from bs4 import BeautifulSoup

# Remove all extra spaces
def remove_spaces(string):
    return " ".join(string.split())

url = 'https://www.wsj.com/news/archive/2022/02/10?page='
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}

relevant_headlines = ["Business", "Finance"] #"Markets", "Finance", "Financial", "Earnings"]
for i in range(1, 6): # pages 1-5, will not return error if not seen
    soup = BeautifulSoup(requests.get(url+str(i), headers=headers).content, 'html.parser')

    for article in soup.select('article'):

        for keyword in relevant_headlines:
            if keyword in article.span.text:

                # article.a["href"]
                blurb = "Title: " + remove_spaces(article.h2.text) + "."
                soup2 = BeautifulSoup(requests.get(article.a["href"], headers=headers).content, 'html.parser')
                for article in soup2.select('article'):
                    blurb += " Summary: " + remove_spaces(article.h2.text) + ". " + remove_spaces(article.p.text)

                #print("What are the names and stock tickers of the companies most associated with the news?\n")
                print("How do you think the stock associated with this news will change?\n")
                print(str("\""+blurb+"\"\n"))

                #print("How will the prices of each of these companies change as a result of this news? Explain.")
                print('-' * 80)
