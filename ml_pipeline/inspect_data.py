import pandas as pd

print("=== URL DATASET ===")
url_df = pd.read_csv("data/processed/url_dataset_clean.csv")
print(url_df.info())
print(url_df.head())
print("Nulls:\n", url_df.isnull().sum())
print("Duplicates:", url_df.duplicated().sum())
print("Labels:\n", url_df.iloc[:, -1].value_counts() if len(url_df.columns) > 1 else "Unknown")

print("\n=== MESSAGE DATASET ===")
msg_df = pd.read_csv("data/processed/message_dataset_clean.csv")
print(msg_df.info())
print(msg_df.head())
print("Nulls:\n", msg_df.isnull().sum())
print("Duplicates:", msg_df.duplicated().sum())
print("Labels:\n", msg_df.iloc[:, -1].value_counts() if len(msg_df.columns) > 1 else "Unknown")
