import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

def generate_synthetic_data(n_samples=1000):
    np.random.seed(42)
    X = []
    y = []
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
        X.append([fights, diplomatic, stealth, risky, cautious])
        y.append(personality)
    return np.array(X), np.array(y)

def train_classifier():
    print("Generating synthetic training data...")
    X, y = generate_synthetic_data(2000)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train_scaled, y_train)
    accuracy = model.score(X_test_scaled, y_test)
    print(f"Model accuracy: {accuracy:.2f}")
    model_dir = os.path.dirname(__file__)
    joblib.dump(model, os.path.join(model_dir, 'personality_classifier.pkl'))
    joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
    print("Model saved.")

if __name__ == '__main__':
    train_classifier()