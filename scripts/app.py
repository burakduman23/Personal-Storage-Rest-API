#!/usr/bin/env python3
import os
import sys
from flask import Flask, jsonify, abort, request, make_response, session, redirect, send_file
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import pymysql
import pymysql.cursors
import cgi, cgitb
import ssl #include ssl libraries
from hashlib import sha256
import shutil





import settings # Our server and db settings, stored in settings.py (Update it properly to your DB setup!)

app = Flask(__name__)
api = Api(app)
#CORS(app)
# Set Server-side session config: Save sessions in the local app directory.
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
Session(app)

savePath = "Storage/"

####################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Bad request' } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Resource not found' } ), 404)

@app.errorhandler(500) # decorators to add to 500 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Internal server error' } ), 500)

class Root(Resource):
	def get(self):
		return app.send_static_file('index.html')

class LogIn(Resource):
	#
	# Set Session and return Cookie
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "Burak", "password": "crapcrap"}' -c cookie-jar -k <login endpoint>
	#
	def post(self):
		if not request.json:
			abort(400) # bad request

		# Parse the json
		
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		if request_params['username'] in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			try:
				dbConnection = pymysql.connect(
					settings.MYSQL_HOST,
					settings.MYSQL_USER,
					settings.MYSQL_PASSWD,
					settings.MYSQL_DB,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)
				cursor = dbConnection.cursor()
				sql = "Select * From Users Where username = %s and password = %s"
				cursor.execute(sql, (request_params['username'], request_params['password'],))
				row = cursor.fetchone()
				if '{username}'.format(**row) == request_params['username']:
					# At this point we have sucessfully authenticated.
					session['username'] = request_params['username']
					response = {'status': 'success' }
					responseCode = 200
			except :
				response = {'status': 'Access denied, try registering'}
				responseCode = 403

		return make_response(jsonify(response), responseCode)

	# GET: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k <login endpoint>

	def delete(self):
		if 'username' in session:
			session.pop('username', None)
			response = {'status': 'success', 'message': 'Successfully removed session'}
			responseCode = 200
		else:
			response = {'status': 'fail', 'message': 'No active session'}
			responseCode = 403
		return make_response(jsonify(response), responseCode)
		

####################################################################################



class Register(Resource):

# curl -i -H "Content-Type: application/json" -X POST -d 
# '{"firstName": "<YOUR NAME>", "lastName" : "<YOUR LAST NAME>", "email" : "<YOUR EMAIL>", "username": "<YOUR USERNAME>", "password": "<YOUR PASSWORD>"}' 
# -c cookie-jar -k <register endpoint>
	def post(self):
		if not request.json:
			
			abort(400) # bad request

		# Parse the json
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('firstName', type=str, required=True)
			parser.add_argument('lastName', type=str, required=True)
			parser.add_argument('email', type=str, required=True)
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)

			request_params = parser.parse_args()
		except:
			abort(400) # bad request
		
		try:
			ldapServer = Server(host=settings.LDAP_HOST)
			ldapConnection = Connection(ldapServer,
				raise_exceptions=True,
				user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
				password = request_params['password'])
			ldapConnection.open()
			ldapConnection.start_tls()
			ldapConnection.bind()
			# At this point we have sucessfully authenticated.
			session['username'] = request_params['username']
# Stuff in here to find the esiting userId or create a use and get the created userId
#check if user is in database
			response = {'status': 'success'}
			responseCode = 201
			dbConnection = pymysql.connect(
				settings.MYSQL_HOST,
				settings.MYSQL_USER,
				settings.MYSQL_PASSWD,
				settings.MYSQL_DB,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			cursor = dbConnection.cursor()
			sql = 'addUser'
			args = (request_params['username'], request_params['firstName'], request_params['lastName'], request_params['password'], request_params['email'], )
			cursor.callproc(sql, args) # stored procedure
			dbConnection.commit()
			rows = cursor.fetchall() # get all the results
			os.mkdir("./"+savePath+request_params['username'])
			print(jsonify(rows))

		except LDAPException:
			response = {'status': 'Access denied'}
			print(response)
			responseCode = 403
		finally:
			ldapConnection.unbind()
		return make_response(jsonify(response), responseCode)


class Documents(Resource):
# curl -i -H "Content-Type: application/json" -b cookie-jar -k <documents endpoint>
	def get(self):

		if 'username' in session:
			owner = session['username']
			response = {'status': 'success'}
			try:
				dbConnection = pymysql.connect(
					settings.MYSQL_HOST,
					settings.MYSQL_USER,
					settings.MYSQL_PASSWD,
					settings.MYSQL_DB,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)
				cursor = dbConnection.cursor()
				cursor.execute("Select doc_name From Documents Where owner ='{}'".format(owner))
				rows = cursor.fetchall()
				responseCode = 200
				response = rows
			except pymysql.Error as e:
				response = {'error' : str(e)}
		else:
			response = {'status': 'fail'}
			responseCode = 403
		return make_response(jsonify({'Documents' :response}),responseCode)
# curl -i -H "Content-Type: application/json" -X POST -F <File content> -b cookie-jar -k <documents endpoint>
	def post(self):
		file = request.files['file']
		if 'file' not in request.files or file.filename == '':
			abort(400)
		
		if 'username' in session:
			owner = session['username']
			try:			
				dbConnection = pymysql.connect(
					settings.MYSQL_HOST,
					settings.MYSQL_USER,
					settings.MYSQL_PASSWD,
					settings.MYSQL_DB,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)
				cursor = dbConnection.cursor()
				sql = 'addDocument'
				args = (file.filename, owner)
				cursor.callproc(sql,args)
				dbConnection.commit()
				path = owner + "/"
				file.save(os.path.join(savePath,path,file.filename))
				response = {'status' : 'added document successfully'}
				responseCode = 200
			except pymysql.Error as e:
				return make_response(jsonify({'error' : str(e)}))
		else:
			response = {'status' : 'You need to login'}
			responseCode = 403
		return make_response(jsonify(response), responseCode)

# curl -i -H "Content-Type: application/json" -X DELETE -d '{"doc_name": "12345.zip", "owner": "mmoustaf"}' -b cookie-jar -k <documents endpoint>
	def delete(self):
		print(request.data)
		if not request.json:
			abort(400)
		parser = reqparse.RequestParser()
		try:
			parser.add_argument('doc_name', type=str, required=True)
			owner = session['username']
			request_params = parser.parse_args()
		except:
			abort(400)
		if 'username' in session:
			try:			
				dbConnection = pymysql.connect(
					settings.MYSQL_HOST,
					settings.MYSQL_USER,
					settings.MYSQL_PASSWD,
					settings.MYSQL_DB,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)
				cursor = dbConnection.cursor()
				sql = 'deleteDocument'
				args = (owner, request_params['doc_name'])
				cursor.callproc(sql, args)
				dbConnection.commit()
				responseCode = 200
				response = {'status' : 'document deleted successfully'}
			except pymysql.Error as e:
				return make_response(jsonify({'error' : str(e)}))
		else:
			response = {'status' : 'You need to login'}
			responseCode = 403
		return make_response(jsonify(response), responseCode)

class User(Resource):

	def delete(self):
		
		if 'username' in session:
			
			try:			
				dbConnection = pymysql.connect(
					settings.MYSQL_HOST,
					settings.MYSQL_USER,
					settings.MYSQL_PASSWD,
					settings.MYSQL_DB,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)
				cursor = dbConnection.cursor()
				sql = 'deleteUser'
				args = (session['username'],)
				cursor.callproc(sql, args)
				dbConnection.commit()
				responseCode = 200
				response = {'status' : 'account and related documents deleted successfully'}
				owner = session['username']				
				shutil.rmtree(os.path.join(savePath,owner))
				session.pop('username', None)

				responseCode = 200
			except pymysql.Error as e:
				return make_response(jsonify({'error' : str(e)}))
		else:
			response = {'status' : 'failure'}
			responseCode = 403
		return make_response(jsonify(response), responseCode)
	
		



	def post(self):
		if not request.json:
			abort(400)
		parser = reqparse.RequestParser()
		try:
			parser.add_argument('doc_name', type=str, required=True)
			owner = session['username']
			request_params = parser.parse_args()
		except:
			abort(400)
		if 'username' in session:
			try:			
				path = owner + "/"
				

			except pymysql.Error as e:
				return make_response(jsonify({'error' : str(e)}))
		else:
			response = {'status' : 'failure'}
			responseCode = 403
		return send_file(os.path.join(savePath,path,request_params['doc_name']), as_attachment=True)
		

# curl -i -H "Content-Type: application/json" -X DELETE -d '{"username": "bduman"}' -b cookie-jar -k https://cs3103.cs.unb.ca:8012/user

	# def delete(self):
	# 	if not request.json:
	# 		abort(400) # bad request

	# 	# Parse the json
	# 	parser = reqparse.RequestParser()
	# 	try:
 	# 		# Check for required attributes in json document, create a dictionary
	# 		parser.add_argument('username', type=str, required=True)
	# 		request_params = parser.parse_args()
	# 	except:
	# 		abort(400) # bad request
	# 	if request_params['username'] == session['username'] and 'username' in session:
	# 		try:			
	# 			dbConnection = pymysql.connect(
	# 				settings.MYSQL_HOST,
	# 				settings.MYSQL_USER,
	# 				settings.MYSQL_PASSWD,
	# 				settings.MYSQL_DB,
	# 				charset='utf8mb4',
	# 				cursorclass= pymysql.cursors.DictCursor)
	# 			cursor = dbConnection.cursor()
	# 			sql = 'deleteUser'
	# 			args = (request_params['username'],)
	# 			cursor.callproc(sql, args)
	# 			dbConnection.commit()
	# 			responseCode = 200
	# 			response = {'status' : 'user account and documents deleted successfully'}
	# 		except pymysql.Error as e:
	# 			return make_response(jsonify({'error' : str(e)}))
	# 	else:
	# 		response = {'status' : 'You need to login'}
	# 		responseCode = 403
	# 	return make_response(jsonify(response), responseCode)
		

api.add_resource(Root,'/')
api.add_resource(LogIn,'/login')
api.add_resource(Register, '/register')
api.add_resource(Documents, '/documents')
api.add_resource(User, '/user')


if __name__ == "__main__":
	#
	# You need to generate your own certificates. To do this:
	#	1. cd to the directory of this app
	#	2. run the makeCert.sh script and answer the questions.
	#	   It will by default generate the files with the same names specified below.
	#
	context = ('cert.pem', 'key.pem') # Identify the certificates you've generated.
	app.run(
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		ssl_context=context,
		debug=settings.APP_DEBUG)
