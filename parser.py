import requests
from bs4 import BeautifulSoup

def parse_book_link_for_meta_data(bookLink):
  htmlString = requests.get(bookLink).content
  bsTree = BeautifulSoup(htmlString,"html.parser")
  title = bsTree.find("h1", attrs={"id": "bookTitle"}).string.strip()
  author = bsTree.find("a", attrs={"class": "authorName"}).span.string.strip()
  rating = bsTree.find("span", attrs={"itemprop": "ratingValue"}).string.strip()
  description = ''.join(bsTree.find("div", attrs={"id": "description"}).find("span", attrs={"style": "display:none"}).stripped_strings)
  return dict(title=title,author=author,rating=float(rating),description=description)

