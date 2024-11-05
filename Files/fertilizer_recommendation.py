# fertilizer_recommendation.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import xgboost as xgb
import pickle

# Load dataset for training
def load_data(filepath="C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Files/fertilizer_recommendation.py"):
    data = pd.read_csv(filepath)
    return data

# Train Random Forest model
def train_rf(X_train, y_train):
    rf_model = RandomForestClassifier(n_estimators=100, random_state=0)
    rf_model.fit(X_train, y_train)
    return rf_model

# Train XGBoost model
def train_xgb(X_train, y_train):
    xgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=0)
    xgb_model.fit(X_train, y_train)
    return xgb_model

# Evaluate model and return accuracy
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return accuracy

# Train and compare models, then save the best one
def train_and_save_best_model():
    data = load_data()
    X = data[['N', 'P', 'K', 'pH', 'moisture', 'crop']]
    y = data['Recommended_Fertilizer']
    
    # Convert categorical crop type to numerical encoding if necessary
    X = pd.get_dummies(X, columns=['crop'], drop_first=True)
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train both models
    rf_model = train_rf(X_train, y_train)
    xgb_model = train_xgb(X_train, y_train)
    
    # Evaluate both models
    rf_accuracy = evaluate_model(rf_model, X_test, y_test)
    xgb_accuracy = evaluate_model(xgb_model, X_test, y_test)
    
    print(f"Random Forest Accuracy: {rf_accuracy * 100:.2f}%")
    print(f"XGBoost Accuracy: {xgb_accuracy * 100:.2f}%")
    
    # Choose the best model based on accuracy
    best_model, best_accuracy, best_model_name = (rf_model, rf_accuracy, "Random Forest") if rf_accuracy >= xgb_accuracy else (xgb_model, xgb_accuracy, "XGBoost")
    print(f"Best model: {best_model_name} with accuracy {best_accuracy * 100:.2f}%")
    
    # Save the best model
    with open("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/fertilizer_recommendation_model.pkl", "wb") as file:
        pickle.dump(best_model, file)
    print(f"{best_model_name} model saved successfully as the best model.")

if __name__ == "__main__":
    train_and_save_best_model()
