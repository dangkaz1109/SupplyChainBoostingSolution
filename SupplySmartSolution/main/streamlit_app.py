import streamlit as st
import requests
import uuid

# --- Page Configuration ---
st.set_page_config(page_title="SupplySmart Churn Prediction", layout="wide")

# --- Page Title and Description ---
st.title("🔮 Customer Churn Prediction")
st.markdown("""
This application demonstrates a full-stack ML pipeline for predicting customer churn.
Enter customer details below to get a churn prediction from the backend API.
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Orchestration**: Custom Python Pipeline
- **Model**: Placeholder (Pre-trained `scikit-learn` model)
""")

# --- API Configuration ---
API_URL = "http://localhost:8000/predict/churn"

# --- Input Form ---
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Customer Details")
    
    # Use a form to group inputs
    with st.form("churn_input_form"):
        customer_id = st.text_input("Customer ID", value=str(uuid.uuid4()))
        tenure = st.slider("Tenure (Months)", 1, 72, 12)
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=18.0, max_value=120.0, value=75.0, step=1.0)
        total_charges = st.number_input("Total Charges ($)", min_value=18.0, max_value=10000.0, value=1000.0)
        contract = st.selectbox("Contract Type", ['Month-to-month', 'One year', 'Two year'])
        payment_method = st.selectbox("Payment Method", ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])
        internet_service = st.selectbox("Internet Service", ['DSL', 'Fiber optic', 'No'])
        
        # Form submission button
        submitted = st.form_submit_button("Predict Churn")

# --- Prediction Logic and Display ---
with col2:
    st.header("Prediction Result")
    
    if submitted:
        # 1. Create payload from form data
        payload = {
            "customer_id": customer_id,
            "tenure": tenure,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
            "Contract": contract,
            "PaymentMethod": payment_method,
            "InternetService": internet_service
        }
        
        # 2. Call the API
        try:
            with st.spinner("Calling prediction API..."):
                response = requests.post(API_URL, json=payload)
            
            # 3. Display the result
            if response.status_code == 200:
                result = response.json()
                
                churn_prob = result['churn_probability']
                is_churn = result['churn']
                
                st.subheader(f"Customer: `{result['customer_id']}`")
                
                if is_churn:
                    st.error(f"Prediction: CHURN (Probability: {churn_prob:.2%})")
                    st.write("This customer is likely to churn. Consider taking retention actions.")
                else:
                    st.success(f"Prediction: NO CHURN (Probability: {churn_prob:.2%})")
                    st.write("This customer is likely to stay.")
                
                st.progress(churn_prob)
                st.caption("Note: The prediction is based on a placeholder model and is for demonstration purposes only.")
                
                with st.expander("See Raw API Response"):
                    st.json(result)

            else:
                st.error(f"API Error (Status {response.status_code}):")
                st.json(response.json())
                st.caption("Is the API server running? From the `SupplySmartSolution` directory, run: `python main/api.py`")

        except requests.exceptions.ConnectionError:
            st.error("Connection Error: Could not connect to the API.")
            st.caption(f"Please ensure the backend API is running at `{API_URL}`.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.info("Please fill out the form and click 'Predict Churn'.")

st.markdown("---")
st.caption("SupplySmartSolution Baseline Demo v2.0")
