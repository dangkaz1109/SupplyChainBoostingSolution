
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'churn_processed.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'churn_pipeline.joblib')


def build_pipeline():
    """
    Builds the preprocessing and modeling pipeline.
    """
    # Define preprocessing for numeric and categorical features
    numeric_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
    numeric_transformer = StandardScaler()

    categorical_features = ['Contract', 'PaymentMethod', 'InternetService']
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    # Create a preprocessor object using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='passthrough'
    )

    # Create the full pipeline
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', LogisticRegression(random_state=42))])
    
    return pipeline

def train_pipeline(output_path=MODEL_PATH):
    """
    Orchestrates the training process: Data -> Split -> Train -> Eval -> Save.
    """
    # 1. Get Data
    try:
        df = pd.read_csv(PROCESSED_DATA_PATH)
    except FileNotFoundError:
        print(f"Error: Processed data not found at {PROCESSED_DATA_PATH}")
        return None, 0

    # Handle potential missing values in TotalCharges
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df = df.dropna(subset=['TotalCharges'])

    X = df.drop('Churn', axis=1)
    y = df['Churn']
    
    # 2. Split
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # 3. Build & Train
    print("Training Pipeline (Preprocessor + Logistic Regression)...")
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

if __name__ == '__main__':
    # This allows the script to be run directly to train the model.
    train_pipeline()

