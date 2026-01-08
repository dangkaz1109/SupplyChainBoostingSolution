import sys
import os
import time

# Add the project root to sys.path to ensure imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.mock_data import get_batch_orders
from orchestration.pipeline_manager import SupplyChainPipeline

def main():
    print("\n" + "="*60)
    print(" SupplySmartSolution - Intelligent Supply Chain Baseline ")
    print("="*60 + "\n")
    
    print("[*] Initializing Models...")
    pipeline = SupplyChainPipeline()
    time.sleep(1) # Simulation delay
    
    print("[*] Generating Mock Data (skipping raw CSVs)...")
    orders = get_batch_orders(5)
    print(f"[*] Generated {len(orders)} synthetic orders.\n")
    
    print(f"{ 'Order ID':<10} | { 'Amt ($)':<10} | { 'Mode':<15} | { 'Fraud %':<8} | { 'Risk %':<8} | {'Action'}")
    print("-" * 100)
    
    for order in orders:
        result = pipeline.process_order(order)
        
        # Color coding simulation (using text for broad compatibility)
        fraud_alert = "(!)" if result.is_fraud else "   "
        risk_alert = "(!)" if result.late_delivery_risk else "   "
        
        print(f"{order.order_id:<10} | {order.order_item_total:<10.2f} | {order.shipping_mode:<15} | "
              f"{result.fraud_probability:<8} {fraud_alert} | {result.risk_probability:<8} {risk_alert} | {result.recommended_action}")
        
        time.sleep(0.3)
        
    print("\n" + "="*60)
    print(" Simulation Complete.")
    print("="*60)

if __name__ == "__main__":
    main()
