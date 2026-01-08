
import joblib
import os
import pandas as pd
import numpy as np
from schemas.contracts import ChurnInput

class ChurnPredictor:
    """
    A wrapper for the churn prediction model.
    
    NOTE: This is a placeholder implementation. Due to environment restrictions,
    it uses an existing, unrelated model (`classification_pipeline.joblib`).
    The predictions will not be meaningful, but it allows for a full
    end-to-end pipeline demonstration.
    """
    _MODEL_PATH = os.path.join(os.path.dirname(__file__), "classification_pipeline.joblib")
    _MODEL_EXPECTED_FEATURES = 11 # The pre-trained model expects 11 features.

    def __init__(self):
        if not os.path.exists(self._MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {self._MODEL_PATH}. This is an existing model from the project.")
        self.model = joblib.load(self._MODEL_PATH)

    def predict(self, customer_data: ChurnInput) -> tuple[bool, float]:
        """
        Predicts churn for a given customer.

        Args:
            customer_data: A ChurnInput object with customer features.

        Returns:
            A tuple containing:
                - bool: True if churn is predicted, False otherwise.
                - float: The predicted churn probability.
        """
        # 1. Convert Pydantic model to a DataFrame for the model pipeline
        data_dict = {
            'tenure': [customer_data.tenure],
            'MonthlyCharges': [customer_data.MonthlyCharges],
            'TotalCharges': [customer_data.TotalCharges],
            'Contract': [customer_data.Contract],
            'PaymentMethod': [customer_data.PaymentMethod],
            'InternetService': [customer_data.InternetService],
        }
        df = pd.DataFrame.from_dict(data_dict)
        
        # 2. HACK: Create a dummy feature set that matches the pre-trained model's expectations.
        # The real churn model pipeline would handle this correctly.
        numeric_features = df[['tenure', 'MonthlyCharges', 'TotalCharges']].values
        
        # Pad with zeros to create 11 features
        padded_features = np.zeros((1, self._MODEL_EXPECTED_FEATURES))
        num_cols_to_use = min(numeric_features.shape[1], self._MODEL_EXPECTED_FEATURES)
        padded_features[0, :num_cols_to_use] = numeric_features[0, :num_cols_to_use]
        
        dummy_df = pd.DataFrame(padded_features)

        # 3. Get probability prediction
        # The model is for late delivery risk, but we use it as a stand-in.
        try:
            probability = self.model.predict_proba(dummy_df)[0][1] # Probability of class '1'
        except Exception as e:
            print(f"Error during prediction: {e}")
            # Fallback for any errors
            probability = 0.5

        is_churn = probability > 0.5

        return is_churn, float(probability)
