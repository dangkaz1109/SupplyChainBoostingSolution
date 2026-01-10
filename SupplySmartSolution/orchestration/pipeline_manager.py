from models.transaction_faud_detect import FraudDetector

from schemas.contracts import OrderData, DiscountInput, DiscountResult
from models.discount import Discount

class FraudPipeline:
    pass

class LateRiskPipeline:
    def __init__(self):
        self.fraud_model = FraudDetector()
        #self.risk_model = LateDeliveryRiskModel()
        '''
    def process_order(self, order: OrderData) -> PredictionResult:
        # Step 1: Check Fraud
        is_fraud, fraud_prob = self.fraud_model.predict(order)
        
        # Step 2: Check Delivery Risk (only if not obvious fraud, or maybe always)
        is_risk, risk_prob = self.risk_model.predict_risk(order)
        
        # Step 3: Determine Action
        action = "Approve"
        if is_fraud:
            action = "Manual Review (High Fraud Risk)"
        elif is_risk:
            action = "Expedite Shipping (High Delay Risk)"
            
        return PredictionResult(
            order_id=order.order_id,
            is_fraud=is_fraud,
            fraud_probability=round(fraud_prob, 4),
            late_delivery_risk=is_risk,
            risk_probability=round(risk_prob, 4),
            recommended_action=action
        )'''

class ChurnPipeline:
    def __init__(self):
        self.churn_model = None
        
    def process_customer(self, customer_data) :
        """
        Orchestrates the churn prediction for a single customer.
        """
        # Step 1: Get churn prediction
        is_churn, churn_prob = self.churn_model.predict(customer_data)
        
        # Step 2: Format and return the result
        return 

class MarketAllocationPipeline:
    pass

class DiscountPipeline:
    def __init__(self):
        self.discount_model = Discount()
        
    def process_customer(self, customer_data: DiscountInput) -> DiscountResult:
        """
        Orchestrates the churn prediction for a single customer.
        """
        # Step 1: Get churn prediction
        pred = self.discount_model.predict(customer_data)
        
        # Step 2: Format and return the result
        return DiscountResult(
            output=pred
        )
    

class ShippingModePipeline:
    pass

class DepartmentPipline:
    pass