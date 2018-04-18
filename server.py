from flask import Flask, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'rootr'
mongo = PyMongo(app)


@app.route('/')
def home_page():
	roots={'Potato','Onion','Turnip','Imported Turnip','Imported Garlic' }
	return render_template('home.html',roots=roots)

def get_izhk_balance(IZ_number):
	try:
		citizen = mongo.db.citizens.find_one_or_404({'_id':IZ_number})
		print(citizen)
		return citizen['izhk']
	except Exception as e:
		new_citizen = mongo.db.citizens.insert({'_id':IZ_number,'izhk':100})
		print(new_citizen)
		mongo.db.bulk_write([new_citizen])
		return get_izhk_balance(IZ_number)

def update_izhk_balance(IZ_number,new_balance):
	try:
		updated_citizen = mongo.db.citizens.update_one({'_id':IZ_number},{'$set':{'izhk':new_balance}}) 
		print(mongo.db)
		mongo.db.bulk_write([updated_citizen])
	except Exception as e:
		print (e)


@app.route('/add_bid',methods=['POST'])
def add_bid():
	izhk_balance = get_izhk_balance(request.form['IZ_number'])
	response = ""

	if izhk_balance < int(request.form['bid']):
		response += "<br>You do not have enough Izhk, You have "+ str(izhk_balance)+ \
					" but need "+ request.form['bid']
	else:
		new_balance = izhk_balance - int(request.form['bid'])
		update_izhk_balance(int(request.form['IZ_number']),new_balance)
		response += "<br> Bid successful. New Izhk balace is " + str(new_balance)
	
	response += " <br>You bid for root "+request.form['roots']
	
	response += " <br> Izhk Balance: "+str(new_balance)

	return response 
