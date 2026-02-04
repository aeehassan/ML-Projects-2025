import streamlit as st 
import pandas as pd
import numpy as np
import joblib as jb
# https://plotly.com/python-api-reference/plotly.express.html
import plotly.express as px

# Title
st.title('⚒️ Multi Design')

# Loading model and other components
ss, model = jb.load('eed.pkl')

# Upload section
## Uploader
st.markdown('### Upload Designs')
uploaded_file = st.file_uploader('',type='csv')

## Preview uploaded file
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.markdown('##### Data preview')
    ### Format the dataframe 
    row_height = 35
    n_rows = 5
    height=row_height * (n_rows + 1) # +1 for header
    edited_df = st.data_editor(df, height=height)  
    ### To avoid exporting the indices
    # Download button without index column
    csv = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        csv,
        file_name="data.csv",
        # To tell the browser the kind of file that is being downloaded
        mime="text/csv" 
    )

    # Output section
    st.markdown('### Output')
    ## Y1 and Y2 values
    st.markdown('##### 🔃 Heating and Cooling Load')
    ### Predicting the targets
    # Standardization
    ## Returns an array
    cols = edited_df.columns
    edited_df = ss.transform(edited_df)
    ## Transform to a df
    edited_df = pd.DataFrame(edited_df, columns=cols)
    
    # Prediction 
    pred = model.predict(edited_df).round(2)
    pred = pd.DataFrame(pred, columns=['HL','CL'])
    pred['Demand'] = pred['HL'] + pred['CL']
    
    if st.button('🔮 Predict Heating & Cooling Load'):
        st.dataframe(pred, height=height)
    
    ## Graphical representation -- Scatter Plots, Bar chart, Box plots and Ranking chart
    st.markdown('##### 📊 Visualizations')
    choices = ["Scatter Plot", "Bar Chart", "Box Plot", "Ranking Chart"]
    plot_choice = st.selectbox("📌 Select Visualization", choices)

    # Scatter Plot
    if plot_choice == "Scatter Plot":
        fig = px.scatter(
            pred,
            x="HL",
            y="CL",
            text=pred.index,
            color=pred.index,
            title="Heating Load vs Cooling Load"
        )
        fig.update_traces(marker_size=15)
        st.plotly_chart(fig, use_container_width=True)

    # Bar Chart
    #####
    elif plot_choice == "Bar Chart":
        # index(D) -> HL and CL
        subset = pred.head(5).reset_index(names="Design")
        fig = px.bar(
            subset.melt(id_vars="Design", value_vars=["HL", "CL"], var_name="Load Type", value_name="Value"),
            x="Design",
            y="Value",
            color="Load Type",
            barmode="group",
            title="Comparison of HL and CL for Sample Designs"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Box Plot
    elif plot_choice == "Box Plot":
        fig = px.box(
            pred.melt(value_vars=["HL", "CL"], var_name="Load Type", value_name="Value"),
            x="Load Type",
            y="Value",
            color="Load Type",
            points='all',
            title="Distribution of Heating and Cooling Load"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Ranking Chart
    elif plot_choice == "Ranking Chart":
        ranking = pred.sort_values("Demand", ascending=True).reset_index(names="Design")
        fig = px.bar(
            ranking,
            x="Design",
            y="Demand",
            title="Ranking of Designs by Total Energy Demand",
            color="Demand",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig, use_container_width=True)
    
        # Highlight top and bottom 3
        st.write("✅ **Most Efficient Designs:**", ranking.head(3)["Design"].tolist())
        st.write("❌ **Least Efficient Designs:**", ranking.tail(3)["Design"].tolist())
        
else:
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
        