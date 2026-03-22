import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# 1. Prepare a more robust training dataset for your demo
# Features: [Length of URL, dot count, has '@' symbol, has '-' symbol]
data = {
    'url_length': [15, 80, 20, 95, 12, 110, 25, 150, 18, 200],
    'dot_count': [1, 5, 1, 4, 1, 6, 2, 8, 1, 10],
    'has_at': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    'has_dash': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    'is_phishing': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # 0=Safe, 1=Phishing
}

df = pd.DataFrame(data)

# 2. Train the Model
X = df.drop('is_phishing', axis=1)
y = df['is_phishing']

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# 3. Save the model in the backend folder
model_path = os.path.join(os.path.dirname(__file__), 'phish_model.pkl')
joblib.dump(model, model_path)

print(f"✅ Success! Brain created and saved at: {model_path}")