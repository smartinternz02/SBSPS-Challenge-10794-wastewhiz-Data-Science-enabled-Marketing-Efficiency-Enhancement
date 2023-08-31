from flask import Flask, render_template, request, session
import pandas as pd
import numpy as np
import os
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = 'ConfigSanta'

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "sNnHt3VkLIzv3uxL99SxCr7cvjXRMhISN8_nKbTCQXuL"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Read the uploaded CSV file using pandas
        test = pd.read_csv(filename)
        
        test['Deal_value'] = test['Deal_value'].str.replace('$', '').str.replace(',', '').astype(float)
        test['Weighted_amount'] = test['Weighted_amount'].str.replace('$', '').str.replace(',', '').astype(float)
        test['Date_of_creation'] = pd.to_datetime(test['Date_of_creation'])
        test.Geography.fillna(method ='ffill', inplace = True)
        test['Designation'] = test['Designation'].replace({'Chairman/CEO/President':'Chairman/CEO/President',
                                              'CEO/Chairman/President':'Chairman/CEO/President',
                                              'Chief Executive Officer':'CEO',
                                              'Vice President / GM (04-present) : VP Sales and Marketing (01-04)':'Vice President/GM'})
        test['Industry'].replace(np.nan,'Banks',inplace=True)
        test['Internal_rating'].replace({-1.00:1.00,82.34:4.00},inplace=True)
        test['Last_lead_update'] = test['Last_lead_update'].map({'Up-to-date':'Up-to-date',
                                        'more than a month':'Pending',
                                        'Following up but lead not responding':'Pending',
                                        '?':'No track',
                                        '2 days back':'Pending','5 days back':'Pending',
                                        'More than 2 weeks':'Pending','More than 2 weeks':'Pending',
                                        'Did not hear back after Level 1':'Pending','More than a week back':'Pending'})
        test['Last_lead_update'].replace(np.nan,'No track',inplace=True)
        test['Last_lead_update'].replace('?','No track',inplace=True)
        test['Location'].replace(np.nan,'Aurangabad',inplace=True)
        test['Weighted_amount'].fillna(test['Weighted_amount'].mean(),inplace=True)
        test['Deal_value'].fillna(test['Deal_value'].mean(),inplace=True)
        test['Weighted_amount'].fillna(test['Weighted_amount'].mean(),inplace=True)
        test['Deal_value'].fillna(test['Deal_value'].mean(),inplace=True)
        test['Resource'] = test['Resource'].map({'We have all the requirements':'Yes',
                                        'Cannot deliver':'No',
                                        'Not enough':'No',
                                        'Deliverable':'Yes'})
        test['Resource'].replace(np.nan,'Yes',inplace=True)
        test_pr=test[['Deal_value','Weighted_amount','Pitch','Lead_revenue']].values.tolist()
        # test_pr = test[[7947,53642.25,'Product_2','100-500 Million']]
        # test_pr_dict = test_pr.to_dict(orient='records')

        # payload_scoring = {"input_data": [{"fields": [['Deal_value','Weighted_amount','Pitch','Lead_revenue']], "values": test_pr_dict}]}
        payload_scoring = {
            "input_data": [
                {
                    "fields": ['Deal_value', 'Weighted_amount', 'Pitch', 'Lead_revenue'],
                    "values": test_pr
                }
            ]
        }
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/44584f11-94e9-40cb-a149-f1161db5f476/predictions?version=2021-05-01', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())  
        if response_scoring.status_code == 200:
                scoring_result = response_scoring.json()
                prediction_values = scoring_result['predictions'][0]['values']
                prediction_df = pd.DataFrame(prediction_values, columns=['Success_probability'])
                final=pd.concat([test['Deal_title'], prediction_df], axis=1)
                final.columns=['Deal_title','Success_probability']
                return render_template('uploaded_data.html', data=final.to_html())
                    
                # return prediction_df  # Return the result as JSON response
        else:
            return "Error in API call", response_scoring.status_code


        # return render_template('uploaded_data.html', data=test.to_html())

if __name__ == '__main__':
    app.run(debug=True)
