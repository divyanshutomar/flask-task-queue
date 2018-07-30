from flask import Flask, request, jsonify
from parser import parse_book_link_for_meta_data
app = Flask(__name__)

# Health check endpoint - responds if service is healthy
@app.route('/')
def health_check():
  return "Web server is up and running!"

# Endpoint that accepts an array of Goodreads URLs for meta information parsing
@app.route('/parseGoodreadsLinks', methods=["POST"])
def parse_goodreads_urls():
  bodyJSON = request.get_json()
  if (isinstance(bodyJSON,list) and len(bodyJSON)):
    bookLinksArray = [x for x in bodyJSON if x.startswith('https://www.goodreads.com/book/show/')]
    if (len(bookLinksArray)):
      return "WIP"
  return "Only array of goodreads book links is accepted.",400

if __name__ == '__main__':
  app.run()