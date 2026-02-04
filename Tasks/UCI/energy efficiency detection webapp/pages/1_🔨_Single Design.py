import streamlit as st 
import pandas as pd
import numpy as np 
import joblib as jb 

# Title
st.title('🔨 Single Design')

# Loading model and other components
ss, model = jb.load('eed.pkl')

# User clarification
st.info('''
        You can only input **one building design** at a time by entering its parameters from **X1 - X8**. 
        Fill in the fields below to get predictions for its Heating Load (HL) and Cooling Load (CL).
        ''')

# Input features using a Form - Building design parameters
with st.form("design_form"):
    col1, col2 = st.columns(2)

    with col1:
        X1 = st.number_input("Relative Compactness", min_value=0.6, max_value=1.0, step=0.01,
                             help="Ratio of the building's compactness (0.5–1). Higher = more compact.")
        X2 = st.number_input("Surface Area", min_value=500.0, max_value=900.0, step=1.0,
                             help="Total surface area of the building in m².")
        X3 = st.number_input("Wall Area", min_value=200.0, max_value=500.0, step=1.0,
                             help="Total wall area of the building in m².")
        X4 = st.number_input("Roof Area", min_value=100.0, max_value=300.0, step=1.0,
                             help="Total roof area of the building in m².")

    with col2:
        X5 = st.number_input("Overall Height", min_value=3.0, max_value=8.0, step=0.5,
                             help="Building height in meters.")
        X6 = st.selectbox("Orientation", [2, 3, 4, 5],
                          help="Orientation coded as integers 2–5 (N, E, S, W).")
        X7 = st.number_input("Glazing Area", min_value=0.0, max_value=0.5, step=0.05,
                             help="Fraction of wall area that is glazed (0–0.5).")
        X8 = st.selectbox("Glazing Area Distribution", [0, 1, 2, 3, 4, 5])

    submitted = st.form_submit_button("🔮 Predict Heating & Cooling Load")

# Prediction
if submitted:
    # Collect inputs into dataframe
    features = pd.DataFrame([[X1, X2, X3, X4, X5, X6, X7, X8]],
                            columns=['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8'])

    # Scale
    features_scaled = ss.transform(features)
    features_scaled = pd.DataFrame(features_scaled, columns=features.columns)

    # Predict
    pred = model.predict(features_scaled)
    
    HL, CL = pred[0]
    total = HL + CL

    # Show results
    st.success(f"🔥 **Heating Load (HL): {HL:.2f} W**")
    st.success(f"❄️ **Cooling Load (CL): {CL:.2f} W**")
    st.success(f"⚡ **Energy Demand: {total:.2f} W**")

st.divider()

# Table of values
st.markdown("### 📋 Accepted Parameter Ranges")
param_ranges = {
    "Relative Compactness": [0.5, 1.0],
    "Surface Area": [300.0, 900.0],
    "Wall Area": [200.0, 500.0],
    "Roof Area": [100.0, 300.0],
    "Overall Height": [3.0, 10.0],
    "Orientation": [2, 5],
    "Glazing Area": [0.0, 0.5],
    "Glazing Area Distribution": [0, 4]
}

ranges_df = pd.DataFrame(param_ranges, index=["Min", "Max"]).T.round(2)
st.table(ranges_df)

