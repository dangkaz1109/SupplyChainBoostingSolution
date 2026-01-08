import random
from schemas.contracts import OrderData

class FraudDetector:
    def predict(self, order: OrderData) -> tuple[bool, float]:
        """
        Returns (is_fraud, probability)
        Logic: High value orders in specific markets are higher risk.
        """
        prob = 0.01 # Base probability
        
        if order.market in ['Africa', 'LATAM']:
            prob += 0.15
            
        if order.order_item_total > 1500:
            prob += 0.50
        elif order.order_item_total > 500:
            prob += 0.10
            
        # Random noise for simulation
        prob += random.uniform(0, 0.05)
        
        return prob > 0.5, min(prob, 0.99)
