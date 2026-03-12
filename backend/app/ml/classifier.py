import joblib
import os
import numpy as np

class PersonalityClassifier:
    def __init__(self):
        """Initialize the classifier with trained model"""
        model_path = os.path.join(os.path.dirname(__file__), 'personality_classifier.pkl')
        scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
        
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.is_trained = True
            print("ML Model loaded successfully!")
        except FileNotFoundError:
            print("Warning: Model not found. Using rule-based fallback.")
            self.is_trained = False
    
    def predict_personality(self, features):
        """
        Predict player personality based on action counts
        features: [fights, diplomatic, stealth, risky, cautious]
        """
        if self.is_trained and sum(features) > 5:  # Only use ML after enough actions
            features_scaled = self.scaler.transform([features])
            prediction = self.model.predict(features_scaled)[0]
            confidence = np.max(self.model.predict_proba(features_scaled))
            
            if confidence > 0.6:  # Only use if confident enough
                return prediction
        
        # Rule-based fallback for early game or low confidence
        return self._rule_based_prediction(features)
    
    def _rule_based_prediction(self, features):
        """Simple rule-based prediction for early game"""
        fights, diplomatic, stealth, risky, cautious = features
        total = sum(features) or 1  # Avoid division by zero
        
        # Calculate percentages
        fight_pct = fights / total
        diplomatic_pct = diplomatic / total
        stealth_pct = stealth / total
        
        if fight_pct > 0.5 and fight_pct > diplomatic_pct and fight_pct > stealth_pct:
            return 'AGGRESSIVE'
        elif diplomatic_pct > 0.5:
            return 'DIPLOMATIC'
        elif stealth_pct > 0.5:
            return 'STEALTHY'
        else:
            return 'BALANCED'