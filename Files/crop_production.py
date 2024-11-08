import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
import lightgbm as lgb
import pickle

def get_clean_data():
    # Load dataset
    data = pd.read_csv("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/Data/crop_production.csv")
    
    # Preprocess 'Year' column to numeric format
    data['Year'] = data['Year'].str[:4].astype(int)
    
    # Drop unnecessary columns
    data = data.drop(['Area Units', 'Production Units', 'Yield', 'State'], axis=1)
    
    # Handle missing values
    data['Production'] = data['Production'].fillna(data['Production'].median())
    data['Area'] = data['Area'].fillna(data['Area'].median())
    data['Crop'] = data['Crop'].fillna(data['Crop'].mode()[0])
    data['Season'] = data['Season'].fillna(data['Season'].mode()[0])
    
    # Normalize specific crop production values
    data.loc[data['Crop'] == 'Cotton(lint)', 'Production'] = (data.loc[data['Crop'] == 'Cotton(lint)', 'Production'] * 170) / 1000
    data.loc[data['Crop'] == 'Jute', 'Production'] = (data.loc[data['Crop'] == 'Jute', 'Production'] * 180) / 1000
    data.loc[data['Crop'] == 'Mesta', 'Production'] = (data.loc[data['Crop'] == 'Mesta', 'Production'] * 180) / 1000
    data.loc[data['Crop'] == 'Coconut', 'Production'] = (data.loc[data['Crop'] == 'Coconut', 'Production'] * 1.5) / 1000
    
    # Log-transform 'Area' and 'Production' columns
    data['Area'] = np.log1p(data['Area'])
    data['Production'] = np.log1p(data['Production'])
    
    # Replace rare categories
    columns = ['District', 'Crop']
    for col in columns:
        freq = data[col].value_counts()
        rare_values = freq[freq < freq.quantile(0.05)].index
        data[col] = data[col].replace(rare_values, f"Other_{col}")
    
    # One-hot encode categorical columns
    data = pd.get_dummies(data, columns=['District', 'Season', 'Crop'], drop_first=True)
    
    return data


def create_model(data):
    # Prepare data
    X = data.drop(['Production'], axis=1)
    y = data['Production']
    
    # Scale the data
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train LightGBM model
    model = lgb.LGBMRegressor(boosting_type='gbdt', num_leaves=40, learning_rate=0.17, n_estimators=30, max_depth=30, random_state=33)
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], eval_metric='l2')
    
    # Model evaluation
    print('Test score: ', model.score(X_test, y_test))
    print('Train score: ', model.score(X_train, y_train))
    
    return model, scaler


def main():
    data = get_clean_data()
    model, scaler = create_model(data)

    # Save the model and scaler
    with open('C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/crop_production_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/crop_production_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)


if __name__ == '__main__':
    main()
