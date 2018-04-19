# Arsh Chauhan
# Last Edited: 04/18/2018
# Server for rootr. System to distribute root vegetables to the citizens of glorious Izkhstan

from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'rootr'
mongo = PyMongo(app)


@app.route('/')
def home_page():
	roots=['Potato','Onion','Turnip','Imported Turnip','Imported Garlic' ]
	return render_template('home.html',roots=roots)

def get_izhk_balance(IZ_number):
	try:
		citizen = mongo.db.citizens.find_one_or_404({'IZ':int(IZ_number)})
		if citizen is not None:
			return citizen['izhk']
	except Exception as e:
		new_citizen = mongo.db.citizens.insert({'IZ':int(IZ_number),'izhk':100})
		return get_izhk_balance(IZ_number)

def update_izhk_balance(IZ_number,new_balance):
	updated_citizen = mongo.db.citizens.find_one_and_update({"IZ":IZ_number},{"$set":{"izhk":new_balance}},upsert=True) 

def add_bid_to_db(IZ_number,root,bid_amount):
	mongo.db.bids.insert({"IZ":int(IZ_number),"root":root,"bid":bid_amount})

@app.route('/all_bids_for_citizen/<int:IZ_number>',methods=['GET','POST'])
def get_bids_for_citizen(IZ_number):
	if IZ_number is None:
		IZ_number = request.form['IZ_number']
	bids = mongo.db.bids.find({'IZ':IZ_number})
	bids_list=[]
	for bid in bids:
		bids_list.append({'root':bid['root'],'izhk':bid['bid']})
	print (bids_list)
	return jsonify(bids_list)
	

@app.route('/add_bid',methods=['POST'])
def add_bid():
	izhk_balance = get_izhk_balance(request.form['IZ_number'])
	response = ""

	if izhk_balance < int(request.form['bid']):
		response += "<br>You do not have enough Izhk, You have "+ str(izhk_balance)+ \
					" but need "+ request.form['bid']
		new_balance = izhk_balance
	else:
		new_balance = izhk_balance - int(request.form['bid'])
		add_bid_to_db(int(request.form['IZ_number']),request.form['roots'],int(request.form['bid']))
		update_izhk_balance(int(request.form['IZ_number']),new_balance)
		response += "<br> Bid successful. New Izhk balace is " + str(new_balance)
	
	response += " <br>You bid for root "+request.form['roots']
	
	response += " <br> Izhk Balance: "+str(new_balance)

	return response 
