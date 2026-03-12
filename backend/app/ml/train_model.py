import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

def generate_synthetic_data(n_samples=1000):
    """Generate synthetic player data for training"""
    np.random.seed(42)
    
    data = []
    personalities = ['AGGRESSIVE', 'DIPLOMATIC', 'STEALTHY', 'BALANCED']
    
    for _ in range(n_samples):
        personality = np.random.choice(personalities)
        
        if personality == 'AGGRESSIVE':
            fights = np.random.randint(15, 30)
            diplomatic = np.random.randint(0, 10)
            stealth = np.random.randint(0, 10)
            risky = np.random.randint(15, 30)
            cautious = np.random.randint(0, 10)
        
        elif personality == 'DIPLOMATIC':
            fights = np.random.randint(0, 10)
            diplomatic = np.random.randint(15, 30)
            stealth = np.random.randint(5, 15)
            risky = np.random.randint(0, 10)
            cautious = np.random.randint(15, 30)
        
        elif personality == 'STEALTHY':
            fights = np.random.randint(5, 15)
            diplomatic = np.random.randint(5, 15)
            stealth = np.random.randint(15, 30)
            risky = np.random.randint(10, 20)
            cautious = np.random.randint(10, 20)
        
        else:  # BALANCED
            fights = np.random.randint(10, 20)
            diplomatic = np.random.randint(10, 20)
            stealth = np.random.randint(10, 20)
            risky = np.random.randint(10, 20)
            cautious = np.random.randint(10, 20)
        
        data.append({
            'fights': fights,
            'diplomatic': diplomatic,
            'stealth': stealth,
            'risky': risky,
            'cautious': cautious,
            'personality': personality
        })
    
    return pd.DataFrame(data)

def train_classifier():
    """Train and save the personality classifier"""
    print("Generating synthetic training data...")
    df = generate_synthetic_data(2000)
    
    # Prepare features and labels
    feature_cols = ['fights', 'diplomatic', 'stealth', 'risky', 'cautious']
    X = df[feature_cols]
    y = df['personality']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    accuracy = model.score(X_test_scaled, y_test)
    print(f"Model accuracy: {accuracy:.2f}")
    
    # Save model and scaler
    model_path = os.path.join(os.path.dirname(__file__), 'personality_classifier.pkl')
    scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    print(f"Model saved to {model_path}")
    return model, scaler

if __name__ == '__main__':
    train_classifier()