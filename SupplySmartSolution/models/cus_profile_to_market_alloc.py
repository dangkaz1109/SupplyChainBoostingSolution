from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import pandas as pd
import joblib
import os


df = pd.read_csv("SupplySmartSolution\data\processed\supply.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "classification_pipeline.joblib")


def build_pipeline():
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            use_label_encoder=False,
            eval_metric='logloss',
            random_state=42
        ))
    ])
    return pipeline

def train_pipeline(output_path=MODEL_PATH):
    """
    Orchestrates the training process: Data -> Split -> Train -> Eval -> Save.
    """
    # 1. Get Data
    X, y = df.drop('Late_delivery_risk', axis=1), df['Late_delivery_risk']
    
    # 2. Split
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Build & Train
    print("Training Pipeline (Scaler + XGB)...")
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    # 4. Evaluate
    print("\n--- Model Evaluation ---")
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))

    # 5. Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump(pipeline, output_path)
    print(f"\nPipeline saved to {output_path}")
    return pipeline, acc

def load_trained_model(path=MODEL_PATH):
    """
    Loads the serialized model.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found at {path}. Run training first.")
    return joblib.load(path)

def predict(model, data):
    """
    Wrapper for prediction. 
    data: pandas DataFrame or 2D array.
    """
    return model.predict(data)