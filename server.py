from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
import pickle
import rq_dashboard
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

# Spawn a client connection to redis server. Here Docker
# provieds a link to our local redis server usinf 'redis'
redisClient = Redis(host='redis')

# Initialize a redis queue instance with name 'bookInfoParser'.
# This name will be used while declaring worker process so that it can 
# start processing tasks in it.
bookInfoParserQueue = Queue('bookInfoParser',connection=redisClient)

#################################
###### Methods ##################
#################################

generate_redis_key_for_book = lambda bookURL: 'GOODREADS_BOOKS_INFO:' + bookURL

def parse_book_link_for_meta_data(bookLink):
  htmlString = requests.get(bookLink).content
  bsTree = BeautifulSoup(htmlString,"html.parser")
  title = bsTree.find("h1", attrs={"id": "bookTitle"}).string
  author = bsTree.find("a", attrs={"class": "authorName"}).span.string
  rating = bsTree.find("span", attrs={"itemprop": "ratingValue"}).string
  description = ''.join(bsTree.find("div", attrs={"id": "description"}).find("span", attrs={"style": "display:none"}).stripped_strings)
  return dict(title=title.strip() if title else '',author=author.strip() if author else '',rating=float(rating.strip() if rating else 0),description=description)

def parse_and_persist_book_info(bookUrl):
  redisKey = generate_redis_key_for_book(bookUrl)
  bookInfo  = parse_book_link_for_meta_data(bookUrl)
  redisClient.set(redisKey,pickle.dumps(bookInfo))


#################################
#### ENDPOINTS ##################
#################################

# Health check endpoint - responds if service is healthy
@app.route('/')
def health_check():
  return "Web server is up and running!"

# Endpoint that accepts an array of Goodreads URLs for meta information parsing
@app.route('/parseGoodreadsLinks', methods=["POST"])
def parse_goodreads_urls():
  bodyJSON = request.get_json()
  if (isinstance(bodyJSON,list) and len(bodyJSON)):
    bookLinksArray = [x for x in list(set(bodyJSON)) if x.startswith('https://www.goodreads.com/book/show/')]
    if (len(bookLinksArray)):
      for bookUrl in bookLinksArray:
        bookInfoParserQueue.enqueue_call(func=parse_and_persist_book_info,args=(bookUrl,),job_id=bookUrl)
      return "%d books are scheduled for info parsing."%(len(bookLinksArray))
  return "Only array of goodreads book links is accepted.",400

# Endpoint for retrieving book info from Redis
@app.route('/getBookInfo', methods=["GET"])
def get_goodreads_book_info():
  bookURL = request.args.get('url', None)
  if (bookURL and bookURL.startswith('https://www.goodreads.com/book/show/')):
    redisKey = generate_redis_key_for_book(bookURL)
    cachedValue = redisClient.get(redisKey)
    if cachedValue:
      return jsonify(pickle.loads(cachedValue))
    return "No meta info found for this book."
  return "'url' query parameter is required. It must be a valid goodreads book URL.",400

######################################
## Integrating RQ Dashboard with flask
######################################
app.config.from_object(rq_dashboard.default_settings)
app.config.update(REDIS_URL='redis://redis')
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rqstatus")


if __name__ == '__main__':
  app.run()
