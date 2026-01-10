import joblib
import os
import pandas as pd
import numpy as np
from schemas.contracts import DiscountInput

class Discount: 
    def __init__(self):
        pass
    def predict(self, data: DiscountInput) -> float:
        return 20
    

