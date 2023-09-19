import requests
from bs4 import BeautifulSoup

import os
from json import dump


def parse_quotes():
    url = "http://quotes.toscrape.com/page/"
    page = 1
    res_list = []
    while True:
        html = requests.get(url + f"{page}/")
        if html.status_code == 200:
            if "No quotes found!" not in html.text:
                soup = BeautifulSoup(html.text, "html.parser")
                quotes = soup.select("div[class=quote] span[class=text]")
                authors = soup.select(
                    "div[class=quote] span small[class = author]")
                tags = soup.find_all('div', class_='tags')
                for i in range(0, len(quotes)):
                    tags_for_quote = tags[i].find_all('a', class_='tag')
                    tags_list = []
                    for tag_for_quote in tags_for_quote:
                        tags_list.append(tag_for_quote.text)
                    quote_dict = {"tags": tags_list,
                                  "author": authors[i].text,
                                  "quote": quotes[i].text}
                    res_list.append(quote_dict)
                page += 1
            else:
                break
    dump_quotes(res_list)


def parse_authors_links():
    page = 1
    url = "http://quotes.toscrape.com/page"
    links_author = []
    while True:
        html = requests.get(url + f"/{page}/")
        if html.status_code == 200:
            if "No quotes found!" not in html.text:
                soup = BeautifulSoup(html.text, "html.parser")
                authors = soup.select("div[class=quote] span a")
                for author in authors:
                    links_author.append(url.removesuffix(
                        "/page") + str(author["href"]))
                page += 1
            else:
                break
    parse_authors(links_author)


def parse_authors(links_author: list):
    authors_list = []
    for link in links_author:
        html = requests.get(link)
        soup = BeautifulSoup(html.text, "html.parser")
        author_fullname = soup.find('div', class_="author-details").find('h3')
        born_date = soup.find(
            'div', class_="author-details").find('p').find('span', class_="author-born-date")
        born_location = soup.find(
            'div', class_="author-details").find('p').find('span', class_="author-born-location")
        description = soup.find(
            'div', class_="author-details").find('div', class_="author-description")
        author_dict = {"name": author_fullname.text,
                       "born_date": born_date.text,
                       "born_location": born_location.text,
                       "description": description.text.strip()}
        if author_dict not in authors_list:
            authors_list.append(author_dict)
    dump_authors(authors_list)
    return authors_list


def dump_authors(authors):
    with open("results/authors.json", "w", encoding="utf-8") as fd:
        dump(authors, fd, indent=2, ensure_ascii=False)


def dump_quotes(quotes: list):
    with open("results/quotes.json", "w", encoding="utf-8") as fd:
        dump(quotes, fd, indent=2, ensure_ascii=False)


def main():
    new_path = r'.\results'
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    parse_quotes()
    parse_authors_links()


# python main.py
if __name__ == '__main__':
    main()
