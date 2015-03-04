import web
import csv
import os.path
import psycopg2
import sys
import pprint
urls = (
  '/input', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('templates/')


class Index(object):	
    def GET(self):
        return render.input_form()

    def POST(self):
        
	form=web.input()
	if not form.Path:
		return('No path was Provided')
	with open(form.Path) as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
		conn_string = "host='localhost' dbname='postgres' user='postgres' password='poonam'"
		# print the connection string we will use to connect
		print "Connecting to database\n	->%s" % (conn_string)
 
		# get a connection, if a connect cannot be made an exception will be raised here
		conn = psycopg2.connect(conn_string)
 
		# conn.cursor will return a cursor object, you can use this cursor to perform queries
		cursor = conn.cursor()
    		for row in spamreader:       
			#print ', '.join(row)
			# execute our Query
			cursor.execute("insert into company_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
 			
			# retrieve the records from the database
			#records = cursor.fetchall()
 			conn.commit()
			
			# print out the records using pretty print
			# note that the NAMES of the columns are not shown, instead just indexes.		
		return("File is save in the database")
        	#return render.index(greeting = greeting)

if __name__ == "__main__":
    app.run()
