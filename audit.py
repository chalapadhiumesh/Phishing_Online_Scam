import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import json
import os

def evaluate_model(data_path, text_col, label_col, model_path, name):
    print(f"--- Evaluating {name} ---")
    df = pd.read_csv(data_path)
    print(f"Dataset: {data_path}")
    print(f"Total Records: {len(df)}")
    
    X = df[text_col].fillna("")
    y = df[label_col].astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training Records: {len(X_train)}")
    print(f"Test Records: {len(X_test)}")
    
    model = joblib.load(model_path)
    print(f"Model Pipeline: {model.steps}")
    
    y_pred = model.predict(X_test)
    y_pred = [int(p) for p in y_pred]
    y_test = list(y_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='macro')
    rec = recall_score(y_test, y_pred, average='macro')
    f1 = f1_score(y_test, y_pred, average='macro')
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"F1-score: {f1:.4f}")
    print(f"Confusion Matrix:\n{cm}\n")

if __name__ == "__main__":
    evaluate_model(
        "data/processed/url_dataset_clean.csv", 
        "URL", "target", 
        "models/phishing_url_model_tfidf.joblib", 
        "URL Model"
    )
    evaluate_model(
        "data/processed/message_dataset_clean.csv", 
        "message", "target", 
        "models/scam_message_model.joblib", 
        "Message Model"
    )
