import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

def get_clean_data():
    # Load and prepare the data
    data = pd.read_csv("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/Data/crop_recommendation.csv")
    features = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    target = data['label']
    
    # Encode target labels
    label_encoder = LabelEncoder()
    target_encoded = label_encoder.fit_transform(target)
    
    return features, target_encoded, label_encoder

def create_model(features, target):
    # Scale the data
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        features_scaled, target, test_size=0.2, random_state=42
    )
    
    # Train the RandomForest model
    model = RandomForestClassifier(n_estimators=20, random_state=42)
    model.fit(X_train, y_train)
    
    # Test the model
    y_pred = model.predict(X_test)
    print('Accuracy of our model:', accuracy_score(y_test, y_pred))
    print("Classification report:\n", classification_report(y_test, y_pred))
    
    # Cross-validation
    cv_score = cross_val_score(model, features_scaled, target, cv=5)
    print("Cross Validation Score (Random Forest):", cv_score)
    
    return model, scaler

def main():
    # Get data and encode labels
    features, target, label_encoder = get_clean_data()
    
    # Train model and scale features
    model, scaler = create_model(features, target)

    # Save model, scaler, and label encoder
    with open('C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/crop_recommendation_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/crop_recommendation_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    with open('C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/crop_recommendation_label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)

if __name__ == '__main__':
    main()
