from flask import Flask
from prometheus_client import make_wsgi_app,Counter,Histogram,Gauge
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time

app=Flask(__name__)

app.wsgi_app= DispatcherMiddleware(app.wsgi_app,{'/metrics' : make_wsgi_app()}) # def
REQUEST_COUNTER = Counter('app_http_requests_count','total app http req count',['app_name','endpoint'])
REQUEST_LATENCY= Histogram('app_request_latency','application time per request (latency)',['method','endpoint'])


@app.route('/')
def hello():
    start_time = time.time() # 16000
    REQUEST_COUNTER.labels('prometheus python','/').inc() # increment and assign values for the labels 
    REQUEST_LATENCY.labels('GET','/').observe(time.time()-start_time) #16020-16000 # assign values to lables
    return "<html><head></head><body><h1> hello and welcome </h1></body></html>"

@app.route('/cool')
def cool():
    REQUEST_COUNTER.labels('prometheus python','/cool').inc()
    return "<html><head></head><body><h1> joey dosent share food </h1></body></html>"


if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5005)