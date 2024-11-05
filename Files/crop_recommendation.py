# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pickle
import warnings

warnings.filterwarnings('ignore')

# Load dataset
df = pd.read_csv("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Datasets/crop_recommendation.csv")

# Separate features and target
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

# Encode target labels
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Initialize and train the Random Forest model
rf_model = RandomForestClassifier(n_estimators=20, random_state=0)
rf_model.fit(X_train, y_train_encoded)

# Test accuracy
y_pred = rf_model.predict(X_test)
test_accuracy = accuracy_score(y_test_encoded, y_pred)
print(f"Test Accuracy of Random Forest Model: {test_accuracy * 100:.2f}%")

# Save the trained model and label encoder for future use
with open("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/crop_recommendation_model.pkl", "wb") as file:
    pickle.dump(rf_model, file)

with open("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/crop_recommendation_label_encoder.pkl", "wb") as file:
    pickle.dump(label_encoder, file)

print("Random Forest model and label encoder saved successfully.")
