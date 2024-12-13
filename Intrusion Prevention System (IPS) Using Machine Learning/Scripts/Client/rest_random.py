from flask import Flask,abort,jsonify,request
import pickle
import numpy as np
import pandas as pd
import json
import joblib


model = joblib.load("random_forest_model.pkl")
app = Flask(__name__)

@app.route('/predict',methods=['POST'])
def predict():
	_data=request.get_json()
	data = json.loads(_data)
	df = pd.DataFrame(data)
	np_array = np.array(data)
	
	try:
	    entry_pred = np_array.reshape(1, -1)  
	    
	    pred_res = model.predict(df)
	    print(f"PREDICTION:{pred_res[0]}")
	    return str(pred_res[0])
	except ValueError as e:
	    return jsonify({"error": str(e)}), 400	


if __name__ == '__main__':
	app.run(port=9000,debug=True)