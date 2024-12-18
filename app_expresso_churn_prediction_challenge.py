# -*- coding: utf-8 -*-
"""App Expresso Churn Prediction Challenge.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ut6JpU74DJVBh3jw5reGSbsGSBvWj_qL
"""

import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Expresso Churn Prediction", layout='centered')

# Custom CSS for navigation styling and green theme
custom_css = '''
<style>
body {
    background: linear-gradient(to right, #3bb78f, #0bab64);
    color: #FFFFFF;
    font-family: 'Arial', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Helvetica', sans-serif;
    color: #ffffff;
    text-shadow: 1px 1px 4px #000000;
}

.main {
    background-color: #ffffff;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0px 0px 25px rgba(0,0,0,0.15);
    color: #000000;
}

.sidebar .sidebar-content {
    background: linear-gradient(to bottom, #0bab64, #3bb78f);
    color: #FFFFFF;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.3);
}

.stButton>button {
    background-color: #27ae60;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
}

.stButton>button:hover {
    background-color: #218c53;
}

.stButton>button:focus {
    background-color: #145a32;
}

input[type="number"], select {
    background-color: #e8f5e9;
    color: #1e4620;
    border: none;
    border-radius: 10px;
    padding: 10px;
    box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}

.stMarkdown hr {
    border: none;
    height: 2px;
    background-color: #3bb78f;
    margin-top: 15px;
    margin-bottom: 15px;
}

footer {
    color: #1e4620;
    text-align: center;
    font-weight: bold;
}

.sidebar-navigation {
    margin-bottom: 20px;
}

.sidebar-navigation .active {
    background-color: #218c53;
    color: white;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 10px;
    text-align: center;
    font-weight: bold;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
}

.sidebar-navigation a {
    text-decoration: none;
    display: block;
    padding: 10px;
    color: #FFFFFF;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 10px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
    background-color: #27ae60;
    transition: background-color 0.3s ease;
}

.sidebar-navigation a:hover {
    background-color: #218c53;
}

</style>
'''

# Inject the custom CSS into the app
st.markdown(custom_css, unsafe_allow_html=True)

# Main Title
st.title('Expresso Churn Prediction App')

# Load Data
data = pd.read_csv('Expresso_churn_dataset.csv')
data1 = data.copy()

# Data Cleaning and Preprocessing
del data['user_id'], data['DATA_VOLUME'], data['ORANGE'], data['TIGO'], data['ZONE1'], data['ZONE2'], data['MRG'], data['TOP_PACK'], data['FREQ_TOP_PACK']

data['REGION'].fillna(data['REGION'].mode()[0], inplace=True)
data['MONTANT'].fillna(data['MONTANT'].median(), inplace=True)
data['FREQUENCE_RECH'].fillna(data['FREQUENCE_RECH'].median(), inplace=True)
data['REVENUE'].fillna(data['REVENUE'].median(), inplace=True)
data['ARPU_SEGMENT'].fillna(data['ARPU_SEGMENT'].median(), inplace=True)
data['FREQUENCE'].fillna(data['FREQUENCE'].median(), inplace=True)
data['ON_NET'].fillna(data['ON_NET'].median(), inplace=True)

# Label Encoding
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()

data['REGION'] = label_encoder.fit_transform(data['REGION'])
mapping_dict_region = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))

data['TENURE'] = label_encoder.fit_transform(data['TENURE'])
mapping_dict_tenure = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))

# Train Logistic Regression Model
x = data.drop(['CHURN'], axis=1)
y = data['CHURN']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)
logreg = LogisticRegression()
logreg.fit(x_train, y_train)

# Sidebar Navigation
st.sidebar.header('Navigation')

# Sidebar styled navigation links with active state
nav_choice = st.sidebar.radio("Go to:", ['📊 Visualize Data', '🔮 Predict Churn'], index=0)

# Custom active link highlighting for sidebar
st.sidebar.markdown(f'''
<div class="sidebar-navigation">
    <a href="#visualize" class="{"active" if nav_choice == "📊 Visualize Data" else ""}">📊 Visualize Data</a>
    <a href="#predict" class="{"active" if nav_choice == "🔮 Predict Churn" else ""}">🔮 Predict Churn</a>
</div>
''', unsafe_allow_html=True)

# Visualization Section
if nav_choice == '📊 Visualize Data':
    st.subheader('📊 Data Distribution')
    st.write('Explore how different features are distributed and their relationship with churn:')

    feature = st.selectbox('Select a feature to visualize:', options=['MONTANT', 'REVENUE', 'FREQUENCE_RECH', 'ARPU_SEGMENT', 'ON_NET', 'FREQUENCE'])

    # Create a figure to plot on
    fig, ax = plt.subplots()
    sns.histplot(data[feature], kde=True, ax=ax)

     # Format the axes to make numbers more readable
    ax.ticklabel_format(style='plain')  # Avoid scientific notation
    ax.set_title(f'Distribution of {feature}')
    ax.set_xlabel(feature)
    ax.set_ylabel('Frequency')

     # Adjust the ticks and their labels if necessary
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # Limit number of ticks on x-axis
    ax.yaxis.set_major_locator(plt.MaxNLocator(5))  # Limit number of ticks on y-axis

        # Display the plot using the new method
    st.pyplot(fig)



# Prediction Section
elif nav_choice == '🔮 Predict Churn':
    st.subheader('🔮 Predict Customer Churn')

    region = st.selectbox('Select your region:', data1['REGION'].unique())
    region_map = mapping_dict_region[region]

    tenure = st.selectbox('Select your tenure:', data1['TENURE'].unique())
    tenure_map = mapping_dict_tenure[tenure]

    montant = st.number_input('Enter MONTANT value:')
    frequence_rech = st.number_input('Enter FREQUENCE_RECH:')
    revenue = st.number_input('Enter REVENUE:')
    arpu_segment = st.number_input('Enter ARPU_SEGMENT:')
    frequence = st.number_input('Enter FREQUENCE:')
    on_net = st.number_input('Enter ON_NET:')
    regularity = st.number_input('Enter REGULARITY:')


    my_dict0 ={'REGION': region, 'TENURE' : tenure , 'MONTANT' : montant,
         'FREQUENCE_RECH': frequence_rech , 'REVENUE' : revenue,
          'ARPU_SEGMENT': arpu_segment , 'FREQUENCE':frequence,
          'ON_NET': on_net , 'REGULARITY':regularity ,}
    my_dict0 = pd.DataFrame(my_dict0, index=[0])

    my_dict = pd.DataFrame({'REGION': [region_map], 'TENURE': [tenure_map], 'MONTANT': [montant],
                               'FREQUENCE_RECH': [frequence_rech], 'REVENUE': [revenue],
                               'ARPU_SEGMENT': [arpu_segment], 'FREQUENCE': [frequence],
                               'ON_NET': [on_net], 'REGULARITY': [regularity]})

    if st.button('Show Input Data'):
        st.write(my_dict0)

    if st.button('Predict Churn'):
        y_pred_test = (logreg.predict_proba(my_dict)[:, 1] >= 0.7).astype(int)
        result = 'No Churn' if y_pred_test == 0 else 'Churn'
        st.write(f'Prediction: **{result}**')

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<footer>Made with ❤️ </footer>", unsafe_allow_html=True)