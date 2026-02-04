import streamlit as st
import numpy as np
import joblib
import warnings

# Ignore warnings
warnings.filterwarnings('ignore')
# Bring our model and preprocessing guys in here
ss, model = joblib.load('EESystem.pkl')

# Design the webpage purely with python without any html and css
## Webpage description 
st.title('Energy Efficiency Detection Model')
st.write('This is my model for an energy efficiency system. It takes building design parameters to predict the heating and cooling load of such design')

## Adding the Features -- Streamlit prefers floats as numerical values
# Add padding to the actual min and max values inorder to mimic real world scenario
with st.sidebar:
    x1 = st.number_input('Relative compactness', min_value=0.5, max_value=1.0, help='Min: 0.5 and Max: 1.0')
    x2 = st.number_input('Surface Area', min_value=500.0, max_value=1000.0, step=0.5, help='Min: 500 and Max: 1000')
    x3 = st.number_input('Wall Area', min_value=200.0, max_value=450.0, step=0.5, help='Min: 200 and Max: 450')
    x4 = st.number_input('Roof Area', min_value=100.00, max_value=250.0, step=0.5, help='Min: 100 and Max: 250.0')
    x5 = st.number_input('Overall Height', min_value=3.0, max_value=8.0, help='Min: 3.0 and Max: 8.0')
    x6 = st.number_input('Orientation', min_value=1.0, max_value=6.0, step=1.0, help='1 to 6')
    x7 = st.number_input('Glazing Area', min_value=0.0, max_value=0.5, step=0.05, help='Min: 0.0 and Max: 0.5')
    x8 = st.number_input('Glazing Area Distribution', min_value=0.0, max_value=6.0, step=1.0, help='0 to 6')

# Preprocessing
input_data = [x1,x2,x3,x4,x5,x6,x7,x8]

## Standardization
# [[]] turns our array to 2D which reps the form that our model can take as input
input_data = ss.transform([input_data])

# Compute the target outputs
if st.button('Predict Heating and Cooling Load'):
    # Again we wrap in float coz that's what streamlit wants
    prediction = model.predict(input_data).astype(float)
    st.success(f'Heating Load: {prediction[0][0]:.2f}, Cooling Load: {prediction[0][1]:.2f}')
