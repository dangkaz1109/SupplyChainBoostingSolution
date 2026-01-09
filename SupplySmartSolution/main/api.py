import sys
import os
import uvicorn
from fastapi import FastAPI, HTTPException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from orchestration.pipeline_manager import FraudPipeline, ChurnPipline, LateRiskPipeline, MarketAllocationPipeline, DiscountPipeline, ShippingModePipeline, DepartmentPipline
from schemas.contracts import ChurnInput, ChurnResult, FraudInput, FraudResult, LateRiskInput, LateRiskResult, AllocInput, AllocResult, DiscountInput, DiscountResult, ShipmodeInput, ShipmodeResult     
app = FastAPI(title="SupplySmartSolution API")
pipeline = None

@app.on_event("startup")
def load_pipeline():
    global churn, fraud, late, alloc, discount, shippingmode, department
    try:
        churn = ChurnPipline()
        fraud = FraudPipeline()
        late = LateRiskPipeline()
        alloc = MarketAllocationPipeline()
        discount = DiscountPipeline()
        shippingmode = ShippingModePipeline()
        department = DepartmentPipline()
        print("Customer Churn Pipeline loaded successfully.")
    except Exception as e:
        print(f"Error loading pipeline: {e}")
        pipeline = None

@app.get("/")
def home():
    return {"message": "Welcome to the SupplySmartSolution API. Use the /predict/churn endpoint for predictions."}

@app.post("/predict/churn", response_model=ChurnPredictionResult)
def predict_churn(customer_data: ChurnInput):
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not loaded. Check server logs for errors.")
    
    try:
        result = pipeline.process_customer(customer_data)
        return result
    except FileNotFoundError as e:
         raise HTTPException(status_code=500, detail=f"Model file not found. Ensure 'classification_pipeline.joblib' exists in the models directory.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)


