import os, os.path
import random
import string
import requests, zipfile, io
from datetime import datetime
import pandas as pd
import redis_, json
import ast


import cherrypy


class zerodha(object):
    @cherrypy.expose
    def index(self):
        return open('main.html')

    # API to scrap the latest BhavCopy from the web everyday
    @cherrypy.expose
    def getLatestBhavCopy(self):
        zipFileNameForCsv = 'EQ' + str(datetime.now().day - 1) + str(datetime.now().month) + str(datetime.now().year)[2:] + '.CSV'
        zipfileNameForUrl = 'EQ' + str(datetime.now().day - 1) + str(datetime.now().month) + str(datetime.now().year)[2:] + '_CSV.ZIP'
        zip_file_url = 'https://www.bseindia.com/download/BhavCopy/Equity/' + zipfileNameForUrl
        print(zip_file_url)
        r = requests.get(zip_file_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        redis_.store_data(zipFileNameForCsv)
        return("Done")

    # API to get top ten record from Redis Db
    @cherrypy.expose
    def getTopTenRecordFromRedis(self):
        data = redis_.get_data()
        return (json.dumps(data))

    # API to get the searched keyword stocks
    @cherrypy.expose
    def get_searched_data(self, keyword='*'):
        data = redis_.get_searched_data(keyword)
        return (json.dumps(data))


if __name__ == '__main__':
    # App configs
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    webapp = zerodha()
    cherrypy.quickstart(webapp, '/', conf)
