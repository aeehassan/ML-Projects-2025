import joblib
import streamlit as st
import numpy as np
import pandas as pd
# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

# Web app design
## Current page configuration
st.set_page_config(
    page_title='Bike Rental Predictor', 
    page_icon='🚴‍♂️'
)

## Header and some text
st.title('Bike Rental Prediction Model')
st.write(
    '''Bike sharing systems are new generation of traditional bike rentals where whole process from membership, rental and return back has become automatic. 
    Through these systems, user is able to easily rent a bike from a particular position and return back at another position. Currently, there are about over 500
    bike-sharing programs around the world which is composed of over 500 thousands bicycles. Today, there exists great interest in these systems due to their
    important role in traffic, environmental and health issues.'''
)
st.divider()

# Extract model and components
model = joblib.load('brs.pkl')

## Heading and brief content
st.subheader('Goal')
st.write('The objective of this model is to predict the amount of bike rentals in a given day of the week within a particular month')
st.divider()

## Features within the page 
season = st.number_input('Season', help='1: winter \n 2:spring \n 3:summer \n 4:fall', min_value=1.0, max_value=4.0, step=1.0)
yr = st.number_input('Year', help='0: 2011, 1: 2012', min_value=0.0, max_value=1.0, step=1.0)
month = st.number_input('Month', help='1 to 12', min_value=1.0, max_value=12.0, step=1.0)
holiday = st.number_input('Holiday', help='0: Not holiday \n1: Holiday', min_value=0.0, max_value=1.0, step=1.0)
weekday =st.number_input('Weekday', help='0 - 6', min_value=0.0, max_value=6.0, step=1.0) 
workingday = st.number_input('Working day', help='0: Not working day \n1: Working day', min_value=0.0, max_value=1.0, step=1.0)
weathersit = st.number_input('Weather situation', help='1: Clear \n2: Few clouds \n3: Partly cloudy \n4: Partly cloudy', min_value=1.0, max_value=4.0, step=1.0)
temp = st.number_input('Normalized temperature', help='Values range from 0.05 to 0.86', min_value=0.05, max_value=0.86, step=0.1)
atemp = st.number_input('Normalized feeling temperature', help='Values range from 0.07 to 0.84', min_value=0.07, max_value=0.84, step=0.1)
hum = st.number_input('Normalized humidity', help='Values range from 0 to 100', min_value=0.0, max_value=100.0, step=0.5) / 100.0
windspeed = st.number_input('Normalized windspeed', help='Values range from 0.0 to 0.5', min_value=0.0, max_value=0.5, step=0.1)
day = st.number_input('Day of the month', help='1 to 31', min_value=1.0, max_value=31.0, step=1.0)

## Prediction
inputs = [season,yr,month,holiday,weekday,workingday,weathersit,temp,atemp,hum,windspeed,day]
pred = np.abs(model.predict([inputs]).astype(int))
bikes_count = np.sum(pred)

if st.button('Predict Users'):
    st.success(f'Casual: {pred[0][0]}, Registered: {pred[0][1]}')

if st.button('Rental Bikes Count'):
    st.success(f'Bikes count: {bikes_count}')

    
