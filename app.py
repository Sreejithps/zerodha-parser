"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import os
import json
import csv
import time

from flask import Flask, request, send_file
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/submit',methods = ['POST'])
def result():
    if request.method == 'POST':
        stockdata = json.loads(request.form['text'])
        candles = stockdata['data']['candles']
        if len(candles) == 0:
            return
        with open('download.csv', 'w', newline='') as csvfile:  
            # creating a csv writer object  
            csvwriter = csv.writer(csvfile)  
            for candle in candles:
            # writing the fields  
                stock_time = time.strptime('2017-09-08T00:00:00+0530', '%Y-%m-%dT%H:%M:%S%z')
                candle[0] = time.strftime('%d/%b/%Y', stock_time)
                csvwriter.writerow(candle)  
    try:
        return send_file('download.csv',mimetype="text/csv",  as_attachment=True)
    except Exception as e:
        a = str(e)


@app.route('/')
def hello():
    """Renders a sample page."""
    return '<html>\
                <head><title>Title of the document</title></head>\
                <body>\
                    <form action="/submit" method="POST">\
                        <input type="submit" value="submit"/>\
                        <br/>\
                        <textarea rows="5" cols="100" name="text" placeholder="Paste Zerodha JSON"></textarea>\
                    </form>\
                </body>\
            </html>'

if __name__ == '__main__':
    
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
