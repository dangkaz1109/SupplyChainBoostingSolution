import sys
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from schemas.contracts import DiscountInput
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from orchestration.pipeline_manager import FraudPipeline, LateRiskPipeline, MarketAllocationPipeline, DiscountPipeline, ShippingModePipeline, DepartmentPipline
from schemas.contracts import ChurnInput, ChurnResult, FraudInput, FraudResult, LateRiskInput, LateRiskResult, AllocInput, AllocResult, DiscountInput, DiscountResult, ShipmodeInput, ShipmodeResult     
app = FastAPI(title="SupplySmartSolution API")
discount = None

@app.on_event("startup")
def load_pipeline():
    global discount
    try:
        discount = DiscountPipeline()
        print("DiscountPipeline loaded successfully.")
    except Exception as e:
        print(f"Error loading pipeline: {e}")
        pipeline = None

@app.get("/")
def home():
    return {"message": "Welcome to the SupplySmartSolution API. Use the /predict/discount endpoint for predictions."}

@app.post("/predict/discount", response_model=DiscountResult)
def predict_churn(customer_data: DiscountInput):
    if discount is None:
        raise HTTPException(status_code=503, detail="Pipeline not loaded. Check server logs for errors.")
    
    try:
        result = discount.process_customer(customer_data)
        return result
    except FileNotFoundError as e:
         raise HTTPException(status_code=500, detail=f"Model not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)


