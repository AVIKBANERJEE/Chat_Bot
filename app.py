# "for importing flask"from flask import  Flask
# Creating object of flask
# app=Flask(__name__)
#flask basic structure
#@app.route('/')
# def route():
#     return "Hello"
# if __name__ == "__main__":
#     app.run(debug=True)

#original code starts
from flask import Flask,request,jsonify
import requests

app = Flask(__name__)

@app.route('/',methods=['POST'])
# for extracting the currency,amount,currency-name
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']


    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount,2) # for get the result in 2 decimal place
    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    return jsonify(response)

def fetch_conversion_factor(source,target):

    url = "https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=9c2c141a99ae048b57ca".format(source,target)

    response = requests.get(url)
    response = response.json()
    return response['{}_{}'.format(source,target)]


if __name__ == "__main__":
    app.run(debug=True)