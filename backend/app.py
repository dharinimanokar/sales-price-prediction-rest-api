import numpy as np
import pandas as pd
import joblib
from flask import Flask, jsonify, request

sales_predictor_api = Flask('Superkart Sales Predictor API')
model = joblib.load('sales_forecast_prediction_model_v1_0.joblib')

@sales_predictor_api.get("/")
def home():
  '''
  This function handles GET requests to the root URL ('/') of the API.
  It returns a simple welcome message.
  '''
  return "Welcome to SuperKart Sales Prediction API!"

@sales_predictor_api.post("/v1/sales")
def predict_sales():
    '''
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted sales price as a JSON response.
    '''
    property_data = request.get_json()
    sample = {
        "Product_Weight": property_data['Product_Weight'],
        "Product_Sugar_Content": property_data['Product_Sugar_Content'],
        "Product_Allocated_Area": property_data['Product_Allocated_Area'],
        "Product_MRP": property_data['Product_MRP'],
        "Store_Size": property_data['Store_Size'],
        "Store_Location_City_Type": property_data['Store_Location_City_Type'],
        "Store_Type": property_data['Store_Type'],
        "Product_Id_char": property_data['Product_Id_char'],
        "Store_Age_Years": property_data['Store_Age_Years'],
        "Product_Type_Category": property_data['Product_Type_Category'],
        }
          

      # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

      # Make prediction (get log_price)
    predicted_price = model.predict(input_data)[0]

      # Convert predicted_price to Python float
    predicted_price = round(float(predicted_price), 2)
      # The conversion above is needed as we convert the model prediction (log price) to actual price using np.exp, which returns predictions as NumPy float32 values.
      # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

      # Return the actual price
    return jsonify({'Predicted Price (in dollars)': predicted_price})

  # Define an endpoint for batch prediction (POST request)
@sales_predictor_api.post('/v1/salesbatch')
def predict_sales_price_batch():
    """
    This function handles POST requests to the '/v1/salesbatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predicted_prices = model.predict(input_data).tolist()

    # Calculate actual prices
    predicted_prices = [round(float(predicted_price), 2) for predicted_price in predicted_prices]

    input_data['Predicted_Sales'] = predicted_prices

    return input_data.to_json(orient='records')

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    sales_predictor_api.run(debug=True)

