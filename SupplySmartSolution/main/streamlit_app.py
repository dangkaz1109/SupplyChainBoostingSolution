import streamlit as st
import requests
import uuid
from schemas.contracts import DiscountInput
# --- Page Configuration ---
st.set_page_config(page_title="SupplySmart Churn Prediction", layout="wide")

# --- Page Title and Description ---
st.title("Discount")
st.markdown("""
This application demonstrates a full-stack ML pipeline for predicting customer churn.
Enter customer details below to get a churn prediction from the backend API.
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Orchestration**: Custom Python Pipeline
- **Model**: Placeholder (Pre-trained `scikit-learn` model)
""")

# --- API Configuration ---
API_URL = "http://localhost:8000/predict/discount"

# --- Input Form ---
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Customer Data")
    
    # Use a form to group inputs
    with st.form("churn_input_form"):
        total_charges = st.number_input("Data: ")
        
        # Form submission button
        submitted = st.form_submit_button("Discount")

# --- Prediction Logic and Display ---
with col2:
    st.header("Discount Result")
    
    if submitted:
        # 1. Create payload from form data
        inp = DiscountInput(data = total_charges)
        payload = inp.model_dump()
        
        # 2. Call the API
        try:
            with st.spinner("Calling prediction API..."):
                response = requests.post(API_URL, json=payload)
            
            # 3. Display the result
            if response.status_code == 200:
                result = response.json()
                
                
                ressult = result['output']
                
                st.write(f"{ressult:.2%}")
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
