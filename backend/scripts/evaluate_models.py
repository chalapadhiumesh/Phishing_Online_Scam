import pandas as pd
import joblib
import os
import sys
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, average_precision_score

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)

def evaluate_message_model():
    print("=== Evaluating Message Model ===")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Check if new model exists, else fallback to old path for testing
    model_path = os.path.join(base_dir, 'backend', 'models', 'scam_message_model.joblib')
    if not os.path.exists(model_path):
        model_path = os.path.join(base_dir, 'models', 'scam_message_model.joblib')
    
    data_path = os.path.join(base_dir, 'data', 'processed', 'message_dataset_clean.csv')
    
    if not os.path.exists(model_path) or not os.path.exists(data_path):
        print("Model or dataset not found.")
        return
        
    pipeline = joblib.load(model_path)
    df = pd.read_csv(data_path)
    X = df['message']
    y = df['target']
    
    y_pred = pipeline.predict(X)
    y_proba = pipeline.predict_proba(X)[:, 1]
    
    precision = precision_score(y, y_pred)
    recall = recall_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    roc_auc = roc_auc_score(y, y_proba)
    pr_auc = average_precision_score(y, y_proba)
    cm = confusion_matrix(y, y_pred)
    
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"ROC-AUC: {roc_auc:.4f}")
    print(f"PR-AUC: {pr_auc:.4f}")
    print("Confusion Matrix:")
    print(cm)
    
    print("\nTesting Adversarial Examples:")
    examples = [
        "URGENT: Click here to claim your prize.",
        "Your account has been suspended. Please log in immediately.",
        "Hey, are we still on for lunch tomorrow?",
    ]
    preds = pipeline.predict(examples)
    for ex, p in zip(examples, preds):
        print(f"'{ex}' -> {'Phishing/Spam (1)' if p == 1 else 'Legitimate (0)'}")
    print("\n")

def evaluate_url_model():
    print("=== Evaluating URL Combined Model ===")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    model_path = os.path.join(base_dir, 'backend', 'models', 'phishing_url_model_combined.joblib')
    if not os.path.exists(model_path):
        model_path = os.path.join(base_dir, 'models', 'phishing_url_model_combined.joblib')
        
    data_path = os.path.join(base_dir, 'data', 'processed', 'url_dataset_clean.csv')
    
    if not os.path.exists(model_path) or not os.path.exists(data_path):
        print("Model or dataset not found.")
        return
        
    pipeline = joblib.load(model_path)
    df = pd.read_csv(data_path)
    X = df['URL'].fillna("")
    y = df['target'].astype(int)
    
    y_pred = pipeline.predict(X)
    try:
        y_proba = pipeline.predict_proba(X)[:, 1]
        roc_auc = roc_auc_score(y, y_proba)
        pr_auc = average_precision_score(y, y_proba)
    except Exception:
        roc_auc = 0.0
        pr_auc = 0.0
    
    precision = precision_score(y, y_pred)
    recall = recall_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    cm = confusion_matrix(y, y_pred)
    
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"ROC-AUC: {roc_auc:.4f}")
    print(f"PR-AUC: {pr_auc:.4f}")
    print("Confusion Matrix:")
    print(cm)
    
    print("\nTesting Adversarial Examples:")
    examples = [
        "http://secure-login-update.com/verify",
        "https://www.google.com",
        "http://claim-your-prize.free-money.biz"
    ]
    preds = pipeline.predict(examples)
    for ex, p in zip(examples, preds):
        print(f"'{ex}' -> {'Legitimate (1)' if p == 1 else 'Phishing (0)'}")
    print("\n")

if __name__ == "__main__":
    evaluate_message_model()
    evaluate_url_model()
