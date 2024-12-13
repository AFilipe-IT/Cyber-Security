from flask import Flask,abort,jsonify,request
import pickle
import numpy as np
import pandas as pd
import json
import joblib

model = joblib.load("svm_model.pkl")
modelRandom = joblib.load("random_forest_model.pkl")
#model = pickle.load(open("svm_model.pkl","rb"))


app = Flask(__name__)

@app.route('/predict',methods=['POST'])
def predict():

	data=request.get_json()
	np_array = np.array(data)

	try:
	    entry_pred = np_array.reshape(1, -1)  
	    pred_res = model.predict(np_array.reshape(1, -1))
	    print(f"PREDICTION:{pred_res[0]}")
	    return str(pred_res[0])
	except ValueError as e:
	    return jsonify({"error": str(e)}), 400	

@app.route('/predictRandom',methods=['POST'])
def predictRandom():
	_data=request.get_json()
	data = json.loads(_data)
	df = pd.DataFrame(data)
	np_array = np.array(data)
	
	try:
	    entry_pred = np_array.reshape(1, -1)  
	    
	    pred_res = modelRandom.predict(df)
	    print(f"PREDICTION:{pred_res[0]}")
	    return str(pred_res[0])
	except ValueError as e:
	    return jsonify({"error": str(e)}), 400	

if __name__ == '__main__':
	app.run(port=9000,debug=True)