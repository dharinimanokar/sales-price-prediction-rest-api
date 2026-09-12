import streamlit as st
import pandas as pd
import requests

BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Prediction")

st.subheader("Online Prediction")

product_type_category = {
    "Perishables": ['Frozen Foods', 'Dairy', 'Meat', 'Seafood', 'Fruits and Vegetables', 'Breads'],
    "Non Perishables": ['Health and Hygiene', 'Household', 'Hard Drinks', 'Soft Drinks',
                         'Canned', 'Baking Goods', 'Snack Foods', 'Breakfast', 'Starchy Foods', 'Others']
}

def get_category(product_type):
    for category, types in product_type_category.items():
        if product_type in types:
            return category
    return "Non Perishables"  # fallback default

product_id = st.text_input("Product ID", "FD1234")
product_type = st.selectbox("Product Type", [
    'Frozen Foods', 'Dairy', 'Canned', 'Baking Goods', 'Snack Foods', 'Meat',
    'Breakfast', 'Seafood', 'Fruits and Vegetables', 'Breads',
    'Health and Hygiene', 'Household', 'Hard Drinks', 'Soft Drinks', 'Others', 'Starchy Foods'
])
establishment_year = st.number_input("Store Establishment Year", min_value=1980, max_value=2026, value=2010)
sugar_content = st.selectbox("Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
weight = st.number_input("Product Weight", value=12.66)
allocated_area = st.number_input("Product Allocated Area", value=0.027)
mrp = st.number_input("Product MRP", value=117.08)
store_size = st.selectbox("Store Size", ["High", "Medium", "Small"])
city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Food Mart", "Departmental Store"])

payload = {
  "Product_Weight": weight,
  "Product_Sugar_Content": sugar_content,
  "Product_Allocated_Area": allocated_area,
  "Product_MRP": mrp,
  "Store_Size": store_size,
  "Store_Location_City_Type": city_type,
  "Store_Type": store_type,
  "Product_Id_char": product_id[:2],              # derived, not raw
  "Store_Age_Years": 2026 - establishment_year,
  "Product_Type_Category": get_category(product_type),
}

if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/sales", json=payload)
    st.write(response.json())
    if response.status_code == 200:
        prediction = response.json()['Predicted Price (in dollars)']
        st.success(f"Predicted Sales Price (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/salesbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
