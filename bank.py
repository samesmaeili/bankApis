from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb+srv://exampleUser1:exampleUserPass@cluster0-arukr.mongodb.net/test?retryWrites=true')
db = client.bankData  #database selection


@app.route('/api/signin', methods=['GET'])			#validate a user by checking email and password
def signin():
	email = request.args['email'] 	#get email
	password = request.args['pass'] #get password

	collection1 = db.bankCollection #selecting the collection 
	
	holdUser = collection1.find_one({'email': email})
	if(holdUser is None):
		return jsonify({'message':"Email not found"})
	else:
		if(holdUser['pass'] == password):
			return jsonify({'message':"Ok"})
		else:
			return jsonify({'message':"Password Incorrect"})

	

@app.route('/api/createUser', methods=['GET', 'POST'])		#register a user in bank database
def createUser():
	email = request.args['email'] 	#get email
	password = request.args['pass'] #get password

	collection1 = db.bankCollection #selecting the collection 
	
	holdUser = collection1.find_one({'email': email})

	if(holdUser is None):
		newUser = { 'email': email, 'pass': password } 
		insertion = collection1.insert_one(newUser)

		collection2 = db.moneyCollection #selecting the collection 
		insertion = collection2.insert_one({'email':email, 'amount':0})

		return jsonify({'message':"User Registered"})
	else:
		return jsonify({'message':"Email already in use"})
	


@app.route('/api/removeUser', methods=['GET', 'POST', 'DELETE'])	#remove user from bank database
def removeUser():
	email = request.args['email'] 	#get email

	collection1 = db.bankCollection #selecting the collection 
	
	holdUser = collection1.find_one({'email': email})

	if(holdUser is None):
		return jsonify({'message':"User does not exist"})
	else:
		collection1.remove({'email': email})

		collection2 = db.moneyCollection #selecting the collection 
		collection2.remove({'email': email})

		return jsonify({'message':"User removed"})
	


@app.route('/api/deposit', methods=['GET', 'POST'])
def deposit():
	email = request.args['email'] 	#get email
	amount = request.args['amount'] #get password

	collection1 = db.moneyCollection #selecting the collection 
	
	holdUser = collection1.find_one({'email': email})

	result = collection1.update_many( 
        {'email':email}, 
        { 
                "$set":{ 
                        'amount':int(holdUser['amount'])+int(amount)
                        } 
                  
                } 
        ) 

	return jsonify({'message':"Money deposited"})


@app.route('/api/withdraw', methods=['GET', 'POST'])
def withdraw():
	email = request.args['email'] 	#get email
	amount = request.args['amount'] #get password

	collection1 = db.moneyCollection #selecting the collection 
	
	holdUser = collection1.find_one({'email': email})

	if(int(holdUser['amount']) < int(amount)):
		return jsonify({'message':"Not enough funds"})
	


	result = collection1.update_many( 
        {'email':email}, 
        { 
                "$set":{ 
                        'amount':int(holdUser['amount'])-int(amount)
                        } 
                  
                } 
        ) 

	return jsonify({'message':"Money withdrawn"})



@app.route('/api/getBalance', methods=['GET'])
def getBalance():
	email = request.args['email'] 	#get email

	collection1 = db.moneyCollection #selecting the collection 
	
	holdUser = collection1.find_one({'email': email})
	
	return jsonify({'amount':holdUser['amount']})
	


if __name__ == '__main__':
	app.run(debug=True)