import os
from bottle import run, template, get, post, request

import plotly.plotly as py
from plotly.graph_objs import *
import pandas.io.data as web2
import datetime
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import web
import psycopg2
import sys
import pprint
import HTML


# add your username and api key
py.sign_in("pjain2", "0isnpo0gr1")



@get('/plot')
def form():
    
    return '''<body bgcolor="#E6E6FA">
              <h2>Graph via Plot.ly</h2>
              <form method="POST" action="/plot">
               Search: <input type="text"  name="Search" >
	       <p>Which type of graph would you prefer?</P><br>
	        <input type="radio" name="radio" value="1">Bar
		<input type="radio" name="radio" value="2">Scatter
                <input type="radio" name="radio" value="3">Box <br><br>
		<input type="Reset"/>
                <input type="submit" />
              </form>
	      </body> '''
	 



@post('/plot')
def submit():
    
    # grab data from form
    if not request.forms.get('Search'):
	return('No search was Provided')
    search = request.forms.get('Search')
    if not request.forms.get('radio'):
	return('No Chart Type was Selected')
    radio = request.forms.get('radio')
    
    NewSearch=search
    abc=NewSearch.lower()
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='poonam'"
    print "Connecting to database\n	->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM company_details WHERE company_ticker=%(company_ticker)s OR company_name=%(company_name)s", {'company_ticker': abc ,'company_name':abc} )
    records = cursor.fetchall()
    if(len(records)==0):
	return('No record Found')
    htmlcode = HTML.table(records,header_row=['Company Name','Company Ticker','Company Description','Products','Revenue','Operating Income','Net Income','Total Assets','Total Equity'])
	
    openlist=[1,2,3,4]
    datelist=[1,2,3,4]
    start = datetime.datetime(2014, 11, 25)
    ls_key = 'Adj Close'
    end = datetime.datetime(2014, 12, 01)
    f=web2.DataReader(records[0][1], 'yahoo', start, end)
    cleandata=f.ix['2014-11-25']
    openlist[0]=cleandata.Open
    datelist[0]=start
   
    data=f.ix['2014-11-26']
    openlist[1]=data.Open
    datelist[1]=datetime.datetime(2014, 11, 26)
    
    data1=f.ix['2014-11-28']
    openlist[2]=data1.Open
    datelist[2]=datetime.datetime(2014, 11, 28)

    data2=f.ix['2014-12-01']
    openlist[3]=data2.Open
    datelist[3]=datetime.datetime(2014, 12, 01)

    #print plt.show()
    if(radio=='1'):
   	 data = Data([
        	Bar(
	   	 x=datelist,
            	y=openlist
            
       		 )
    	])
    elif(radio=='2'):
	data = Data([
        	Scatter(
	    	x=datelist,
            	y=openlist
            
        	)
    	])
    elif(radio=='3'):
	 data = Data([
        	Box(
	    	x=datelist,
            	y=openlist
            
        	)
    	])
   
    
    # make api call
    response = py.plot(data, filename='basic-bar')

    if response:
        return (
            '''<body bgcolor="#E6E6FA">
	       <h1>Congrats!</h1>
	    <div>%s</div>
	    <div>	
              View your graph here: <a href="/plot"</a>
	      <br><br>
      	      <iframe width="700" height="400" seamless="seamless" scrolling="no" src="https://plot.ly/~pjain2/0/.embed?width=700&height=500"></iframe>
            </div>
            </body>''' %htmlcode
        )
	

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3086))
    run(host='0.0.0.0', port=port)
