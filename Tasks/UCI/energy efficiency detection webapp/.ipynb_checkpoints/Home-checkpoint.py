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
    page_title='Energy Efficiency Precdictor', 
    page_icon='⚡'
)

## Create page nav
# 1. Create the main page
# 2. Create a folder 'pages'
# 3. Name each page within folder

## Side bar instruction
st.sidebar.success('Select a page above :)')

## Page content 
### Description
st.markdown('# Description')
st.markdown('''
    **Energy efficiency** means how much energy a building needs for the tenants to feel comfortable within it, whether by heating in winter or cooling in summer.
    For example, if two houses are kept at the same cozy temperature in winter, the one that uses less electricity or gas for heating is more energy efficient.
    
    The model we use helps with this by analyzing building designs. Each building design is described by **8 parameters (X1–X8)**, such as glazing area,
    orientation, or other structural features. These parameters act as the inputs to the model.
    
    Based on them, the model predicts two important values: **Heating Load (HL)** and **Cooling Load (CL)**.
    
    - **Heating Load (HL):** how much energy is needed to keep the building warm.
    - **Cooling Load (CL):** how much energy is needed to keep the building cool.
    
    By looking at these predictions, engineers can quickly judge whether a proposed building design will be **energy efficient** or **inefficient**, and then adjust 
    the design accordingly.
    ''')

### Divider
st.divider()

# ### Single Design
# st.markdown('## Single Design')

# ### Multi Design
# st.markdown('## Multi Design')