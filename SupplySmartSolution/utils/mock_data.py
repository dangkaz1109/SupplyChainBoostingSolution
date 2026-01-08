import random
import uuid
from schemas.contracts import OrderData

DEPARTMENTS = ['Fitness', 'Apparel', 'Golf', 'Footwear', 'Outdoors', 'Fan Shop', 'Technology']
MARKETS = ['Pacific Asia', 'USCA', 'Africa', 'Europe', 'LATAM']
CITIES = ['Caguas', 'Chicago', 'Los Angeles', 'Berlin', 'Tokyo', 'Sao Paulo']
SEGMENTS = ['Consumer', 'Corporate', 'Home Office']
SHIP_MODES = ['Standard Class', 'First Class', 'Second Class', 'Same Day']

def generate_mock_order() -> OrderData:
    """Generates a single synthetic order."""
    return OrderData(
        order_id=str(uuid.uuid4())[:8],
        customer_city=random.choice(CITIES),
        customer_segment=random.choice(SEGMENTS),
        department=random.choice(DEPARTMENTS),
        market=random.choice(MARKETS),
        order_item_total=round(random.uniform(10.0, 2000.0), 2),
        shipping_mode=random.choice(SHIP_MODES),
        shipping_date_idx=random.randint(0, 6)
    )

def get_batch_orders(n=10):
    return [generate_mock_order() for _ in range(n)]
