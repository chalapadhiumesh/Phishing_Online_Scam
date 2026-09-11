import pandas as pd
import joblib
import os
import sys
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, average_precision_score

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)

def eval_small():
    print("Evaluating small subset...")
    url_model = joblib.load(os.path.join(base_dir, 'backend', 'models', 'phishing_url_model_combined.joblib'))
    msg_model = joblib.load(os.path.join(base_dir, 'backend', 'models', 'scam_message_model.joblib'))
    
    url_df = pd.read_csv(os.path.join(base_dir, 'data', 'processed', 'url_dataset_clean.csv')).head(500)
    X = url_df['URL'].fillna("")
    y = url_df['target'].astype(int)
    
    y_pred = url_model.predict(X)
    try:
        y_proba = url_model.predict_proba(X)[:, 1]
        roc = roc_auc_score(y, y_proba)
        pr = average_precision_score(y, y_proba)
    except:
        roc, pr = 0.0, 0.0
    print(f"URL: P={precision_score(y, y_pred):.4f}, R={recall_score(y, y_pred):.4f}, F1={f1_score(y, y_pred):.4f}, ROC-AUC={roc:.4f}, PR-AUC={pr:.4f}")
    
    msg_df = pd.read_csv(os.path.join(base_dir, 'data', 'processed', 'message_dataset_clean.csv')).head(500)
    X = msg_df['message']
    y = msg_df['target'].astype(int)
    
    y_pred = msg_model.predict(X)
    try:
        y_proba = msg_model.predict_proba(X)[:, 1]
        roc = roc_auc_score(y, y_proba)
        pr = average_precision_score(y, y_proba)
    except:
        roc, pr = 0.0, 0.0
    print(f"MSG: P={precision_score(y, y_pred):.4f}, R={recall_score(y, y_pred):.4f}, F1={f1_score(y, y_pred):.4f}, ROC-AUC={roc:.4f}, PR-AUC={pr:.4f}")

if __name__ == "__main__":
    eval_small()
