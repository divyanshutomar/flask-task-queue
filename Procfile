webserver: gunicorn --bind "0.0.0.0:5000" server:app
rqworker: rq worker bookInfoParser -u redis://redis
