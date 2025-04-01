import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Get working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Function to load models safely
def load_model(file_name):
    try:
        return pickle.load(open(os.path.join(working_dir, file_name), 'rb'))
    except Exception as e:
        st.error(f"Error loading model {file_name}: {str(e)}")
        return None

# Load models
diabetes_model = load_model('diabetes_model.sav')
heart_disease_model = load_model('heart_disease_model.sav')
parkinsons_model = load_model('parkinsons_model.sav')

# Sidebar for navigation
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System',
                           ['Diabetes Prediction',
                            'Heart Disease Prediction',
                            'Parkinsons Prediction'],
                           menu_icon='hospital-fill',
                           icons=['activity', 'heart', 'person'],
                           default_index=0)

# Function to safely convert inputs to float and replace empty values with 0
def safe_float_conversion(values):
    return [float(x) if x.strip() else 0.0 for x in values]

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction using ML')
    st.markdown("Please enter the following information to predict the likelihood of diabetes.")

    col1, col2, col3 = st.columns(3)
    with col1:
        Pregnancies = st.number_input('Number of Pregnancies', min_value=0, step=1, value=0)
    with col2:
        Glucose = st.number_input('Glucose Level', min_value=0.0, value=0.0)
    with col3:
        BloodPressure = st.number_input('Blood Pressure value', min_value=0.0, value=0.0)
    with col1:
        SkinThickness = st.number_input('Skin Thickness value', min_value=0.0, value=0.0)
    with col2:
        Insulin = st.number_input('Insulin Level', min_value=0.0, value=0.0)
    with col3:
        BMI = st.number_input('BMI value', min_value=0.0, value=0.0)
    with col1:
        DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function value', min_value=0.0, value=0.0)
    with col2:
        Age = st.number_input('Age of the Person', min_value=0, step=1, value=25)

    if st.button('Diabetes Test Result'):
        with st.spinner('Predicting...'):
            user_input = safe_float_conversion([Pregnancies, Glucose, BloodPressure, SkinThickness,
                                                Insulin, BMI, DiabetesPedigreeFunction, Age])
            if diabetes_model:
                diab_prediction = diabetes_model.predict([user_input])
                if diab_prediction[0] == 1:
                    st.error('The person is diabetic')
                else:
                    st.success('The person is not diabetic')
                st.write(f"Prediction: {diab_prediction[0]}")

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction using ML')
    st.markdown("Please enter the following information to predict the likelihood of heart disease.")

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input('Age', min_value=0, step=1, value=50)
    with col2:
        sex = st.selectbox('Sex', ['0', '1'])  # Or ['Male', 'Female']
    with col3:
        cp = st.selectbox('Chest Pain Type', ['0', '1', '2', '3'])
    with col1:
        trestbps = st.number_input('Resting Blood Pressure', min_value=0, value=120.0)
    with col2:
        chol = st.number_input('Serum Cholesterol (mg/dl)', min_value=0.0, value=200.0)
    with col3:
        fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl', ['0', '1'])
    with col1:
        restecg = st.selectbox('Resting ECG Results', ['0', '1', '2'])
    with col2:
        thalach = st.number_input('Max Heart Rate Achieved', min_value=0, value=150)
    with col3:
        exang = st.selectbox('Exercise Induced Angina', ['0', '1'])
    with col1:
        oldpeak = st.number_input('ST Depression Induced by Exercise', min_value=0.0, value=1.0)
    with col2:
        slope = st.selectbox('Slope of Peak Exercise ST Segment', ['0', '1', '2'])
    with col3:
        ca = st.number_input('Major Vessels Colored by Fluoroscopy', min_value=0, max_value=4, step=1, value=0)
    with col1:
        thal = st.selectbox('Thal', ['0', '1', '2'])

    if st.button('Heart Disease Test Result'):
        with st.spinner('Predicting...'):
            user_input = safe_float_conversion([age, sex, cp, trestbps, chol, fbs, restecg, thalach,
                                                exang, oldpeak, slope, ca, thal])
            if heart_disease_model:
                heart_prediction = heart_disease_model.predict([user_input])
                if heart_prediction[0] == 1:
                    st.error('The person has heart disease')
                else:
                    st.success('The person does not have heart disease')
                st.write(f"Prediction: {heart_prediction[0]}")

# Parkinson's Prediction Page
if selected == "Parkinsons Prediction":
    st.title("Parkinson's Disease Prediction using ML")
    st.markdown("Please enter the following information to predict the likelihood of Parkinson's disease.")

    cols = st.columns(3)  # Adjust number of columns as needed
    inputs = ['MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 'MDVP:Jitter(Abs)',
              'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP', 'MDVP:Shimmer', 'MDVP:Shimmer(dB)',
              'Shimmer:APQ3', 'Shimmer:APQ5', 'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR',
              'RPDE', 'DFA', 'Spread1', 'Spread2', 'D2', 'PPE']

    input_values = []
    for i, input_name in enumerate(inputs):
        with cols[i % 3]:  # Example: Distribute across 3 columns
            input_val = st.number_input(input_name, value=0.0)  # Use number_input
            input_values.append(input_val)

    if st.button("Parkinson's Test Result"):
        with st.spinner('Predicting...'):
            user_input = safe_float_conversion(input_values)
            if parkinsons_model:
                parkinsons_prediction = parkinsons_model.predict([user_input])
                if parkinsons_prediction[0] == 1:
                    st.error("The person has Parkinson's disease")
                else:
                    st.success("The person does not have Parkinson's disease")
                st.write(f"Prediction: {parkinsons_prediction[0]}")
