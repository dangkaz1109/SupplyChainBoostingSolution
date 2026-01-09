from pydantic import BaseModel
from typing import Literal

class OrderData(BaseModel):
    order_id: str
    customer_city: str
    customer_segment: Literal['Consumer', 'Corporate', 'Home Office']
    department: str
    market: str
    order_item_total: float
    shipping_mode: Literal['Standard Class', 'First Class', 'Second Class', 'Same Day']
    shipping_date_idx: int  # Simulation of days to ship
    
class ChurnInput(BaseModel):
    customer_id: str
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    Contract: Literal['Month-to-month', 'One year', 'Two year']
    PaymentMethod: Literal['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)']
    InternetService: Literal['DSL', 'Fiber optic', 'No']

class ChurnResult(BaseModel):
    customer_id: str
    churn: bool
    churn_probability: float

class FraudInput(BaseModel):
    pass

class FraudResult(BaseModel):
    pass

class LateRiskInput(BaseModel):
    pass

class LateRiskResult(BaseModel):
    pass

class AllocInput(BaseModel):
    pass

class AllocResult(BaseModel):
    pass

class DiscountInput(BaseModel):
    pass

class DiscountResult(BaseModel):
    pass

class ShipmodeInput(BaseModel):
    pass

class ShipmodeResult(BaseModel):
    pass