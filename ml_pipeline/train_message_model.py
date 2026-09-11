import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os

print("Loading Message Dataset...")
df = pd.read_csv("data/processed/message_dataset_clean.csv")

# Text column: 'message', Target column: 'target' (1 for spam, 0 for ham)
X = df['message']
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Training TF-IDF + Logistic Regression Model...")
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english')),
    ('clf', LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000))
])

pipeline.fit(X_train, y_train)

print("Evaluating...")
y_pred = pipeline.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_dir = os.path.join(base_dir, 'backend', 'models')
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "scam_message_model.joblib")
joblib.dump(pipeline, model_path)
print(f"Model successfully saved to {model_path}")
