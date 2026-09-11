import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import joblib
import os

print("Loading URL Dataset...")
df = pd.read_csv("data/processed/url_dataset_clean.csv")

# Identify numerical features, exclude non-numeric and target columns
exclude_cols = ['URL', 'Domain', 'Title', 'label_name', 'label', 'target', 'original_label']
feature_cols = [c for c in df.columns if c not in exclude_cols and pd.api.types.is_numeric_dtype(df[c])]

print(f"Using {len(feature_cols)} numerical features for URL classification.")
X = df[feature_cols]
y = df['label'] # Assuming 1 is phishing, 0 is legitimate

# Check if there are any missing values that might need imputation
if X.isnull().sum().sum() > 0:
    print("Warning: Missing values found in numerical features. Using SimpleImputer.")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Training Random Forest Classifier... (This might take a moment due to 230k+ rows)")
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('clf', RandomForestClassifier(n_estimators=50, random_state=42, max_depth=15, n_jobs=-1)) # 50 trees, limited depth for speed
])

pipeline.fit(X_train, y_train)

print("Evaluating...")
y_pred = pipeline.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

os.makedirs("models", exist_ok=True)
model_path = "models/phishing_url_model.joblib"
joblib.dump(pipeline, model_path)

# Save feature columns so the backend knows what order to provide them
joblib.dump(feature_cols, "models/url_feature_cols.joblib")

print(f"Model successfully saved to {model_path}")
