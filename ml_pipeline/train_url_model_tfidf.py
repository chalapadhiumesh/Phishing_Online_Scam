import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os

print("Loading URL Dataset for TF-IDF training...")
df = pd.read_csv("data/processed/url_dataset_clean.csv")

# Use the raw URL string
X = df['URL'].fillna("")
y = df['label'] # Assuming 1 is phishing, 0 is legitimate

print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Training TF-IDF + Logistic Regression Model for URLs... (This might take a moment due to 230k+ rows)")
# Character level TF-IDF is often better for URLs, but let's use a mix or just word/char analyzer
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(2, 4), max_features=10000)),
    ('clf', LogisticRegression(random_state=42, max_iter=2000, n_jobs=-1))
])

pipeline.fit(X_train, y_train)

print("Evaluating...")
y_pred = pipeline.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("Classification Report:\n", classification_report(y_test, y_pred))

os.makedirs("models", exist_ok=True)
model_path = "models/phishing_url_model_tfidf.joblib"
joblib.dump(pipeline, model_path)

print(f"Model successfully saved to {model_path}")
