import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

def create_model(data):
    X = data.drop(['Output'], axis=1)
    y = data['Output']
    
    # Scale the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    
    # Train the model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    # Test the model
    y_pred = model.predict(X_test)
    print('Accuracy of our model: ', accuracy_score(y_test, y_pred))
    print("Classification report: \n", classification_report(y_test, y_pred))
    
    return model, scaler

def get_clean_data():
    data = pd.read_csv("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/Data/soil_fertility.csv")
    data['Output'] = data['Output'].map({0: 'Less Fertile', 1: 'Fertile', 2: 'Highly Fertile'})
    return data

def main():
    data = get_clean_data()
    model, scaler = create_model(data)

    with open('C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/soil_fertility_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/soil_fertility_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

if __name__ == '__main__':
    main()
