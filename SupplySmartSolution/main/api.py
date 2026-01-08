import sys
import os
import uvicorn
from fastapi import FastAPI, HTTPException

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from orchestration.pipeline_manager import CustomerChurnPipeline
from schemas.contracts import ChurnInput, ChurnPredictionResult

app = FastAPI(title="SupplySmartSolution API")

# Instantiate the pipeline on startup
pipeline = None

@app.on_event("startup")
def load_pipeline():
    """
    Instantiates the CustomerChurnPipeline when the application starts.
    """
    global pipeline
    try:
        pipeline = CustomerChurnPipeline()
        print("Customer Churn Pipeline loaded successfully.")
    except Exception as e:
        print(f"Error loading pipeline: {e}")
        pipeline = None

@app.get("/")
def home():
    return {"message": "Welcome to the SupplySmartSolution API. Use the /predict/churn endpoint for predictions."}

@app.post("/predict/churn", response_model=ChurnPredictionResult)
def predict_churn(customer_data: ChurnInput):
    """
    Predicts customer churn based on input data.
    """
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not loaded. Check server logs for errors.")
    
    try:
        # Use the pipeline to process the customer data
        result = pipeline.process_customer(customer_data)
        return result
    except FileNotFoundError as e:
         raise HTTPException(status_code=500, detail=f"Model file not found. Ensure 'classification_pipeline.joblib' exists in the models directory.")
    except Exception as e:
        # Catch other potential errors during prediction
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
