import random
from schemas.contracts import OrderData

class LateDeliveryRiskModel:
    def predict_risk(self, order: OrderData) -> tuple[bool, float]:
        """
        Returns (is_late_risk, probability)
        Logic: Standard Class has higher risk than Same Day.
        """
        risk_map = {
            'Standard Class': 0.4,
            'Second Class': 0.25,
            'First Class': 0.1,
            'Same Day': 0.05
        }
        
        base_risk = risk_map.get(order.shipping_mode, 0.2)
        
        # Adjust by Department (e.g. Technology might be more complex to ship)
        if order.department == 'Technology':
            base_risk += 0.1
            
        # Random simulation factor
        actual_risk = base_risk + random.uniform(-0.05, 0.1)
        
        return actual_risk > 0.5, min(max(actual_risk, 0.0), 1.0)
