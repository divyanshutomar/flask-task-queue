from flask import Flask
app = Flask(__name__)

# Health check endpoint - responds if service is healthy
@app.route('/')
def health_check():
  return "Web server is up and running!"

if __name__ == '__main__':
  app.run()