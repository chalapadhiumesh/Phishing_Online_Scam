import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os
import sys

# Add root directory to pythonpath so we can import backend.app.services.features
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app.services.features import URLFeatureExtractor

def train_and_evaluate():
    print("Loading URL Dataset...")
    df = pd.read_csv("data/processed/url_dataset_clean.csv")
    
    X = df['URL'].fillna("")
    y = df['target'].astype(int) # 1 = legitimate, 0 = phishing
    
    print(f"Total records: {len(X)}")
    
    # Stratified split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Building Combined Feature Pipeline...")
    # We use FeatureUnion to concatenate TF-IDF features and structured features
    combined_features = FeatureUnion([
        ('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(2, 4), max_features=10000)),
        ('structured', URLFeatureExtractor())
    ])
    
    # We will use Logistic Regression to prevent overfitting on the synthetic features
    pipeline = Pipeline([
        ('features', combined_features),
        ('clf', LogisticRegression(class_weight='balanced', random_state=42, max_iter=2000, n_jobs=-1))
    ])
    
    print("Training Model...")
    pipeline.fit(X_train, y_train)
    
    print("Evaluating Model...")
    y_pred = pipeline.predict(X_test)
    
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Classification Report:\n", classification_report(y_test, y_pred, target_names=["Phishing (0)", "Legitimate (1)"]))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(base_dir, 'backend', 'models')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "phishing_url_model_combined.joblib")
    joblib.dump(pipeline, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_evaluate()
