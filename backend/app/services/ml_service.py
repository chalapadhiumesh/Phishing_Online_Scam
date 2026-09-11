import joblib
import os
import logging

logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        self.url_model = None
        self.message_model = None
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.url_model_path = os.path.join(base_dir, "backend", "models", "phishing_url_model_combined.joblib")
        self.message_model_path = os.path.join(base_dir, "backend", "models", "scam_message_model.joblib")

    def load_models(self):
        try:
            if os.path.exists(self.url_model_path):
                self.url_model = joblib.load(self.url_model_path)
                logger.info("URL Model loaded successfully.")
            else:
                logger.warning("URL Model not found.")

            if os.path.exists(self.message_model_path):
                self.message_model = joblib.load(self.message_model_path)
                logger.info("Message Model loaded successfully.")
            else:
                logger.warning("Message Model not found.")
        except Exception as e:
            logger.error(f"Error loading models: {e}")

    def predict_url(self, url: str):
        if not self.url_model:
            return {"prediction": "legitimate", "confidence": 0.0, "risk_score": 0, "risk_level": "UNKNOWN", "indicators": ["ML model unavailable"]}
        
        # The pipeline expects a list/array of strings
        proba = self.url_model.predict_proba([url])[0]
        prediction_idx = self.url_model.predict([url])[0] # 0 for phishing, 1 for legitimate
        
        is_phishing = bool(prediction_idx == 0)
        confidence = float(proba[0] if is_phishing else proba[1])
        risk_score = int(proba[0] * 100)
        
        if risk_score >= 80:
            risk_level = "CRITICAL"
        elif risk_score >= 50:
            risk_level = "HIGH"
        elif risk_score >= 20:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
            
        prediction = "phishing" if is_phishing else "legitimate"
        
        indicators = []
        if is_phishing:
            if risk_score >= 80:
                indicators.append("High phishing probability from the ML model")
            else:
                indicators.append("Elevated phishing probability from the ML model")
                
            import re
            suspicious_words = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'confirm']
            if any(w in url.lower() for w in suspicious_words):
                indicators.append("Suspicious account-verification keyword pattern")
            
            if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
                indicators.append("IP address used instead of domain name")
                
            if not url.startswith('https://'):
                indicators.append("Non-secure HTTP connection")
                
            if url.count('-') > 3:
                indicators.append("Unusual URL structure (excessive hyphens)")
        else:
            indicators.append("Low phishing probability based on the trained model")

        return {
            "prediction": prediction,
            "confidence": round(confidence, 4),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "indicators": indicators
        }

    def predict_message(self, message: str):
        if not self.message_model:
            return {"prediction": "legitimate", "confidence": 0.0, "risk_score": 0, "risk_level": "UNKNOWN", "indicators": ["ML model unavailable"]}
        
        proba = self.message_model.predict_proba([message])[0]
        prediction_idx = self.message_model.predict([message])[0] # 1 for scam, 0 for legitimate
        
        is_scam = bool(prediction_idx == 1)
        confidence = float(proba[1] if is_scam else proba[0])
        risk_score = int(proba[1] * 100)
        
        if risk_score >= 80:
            risk_level = "CRITICAL"
        elif risk_score >= 50:
            risk_level = "HIGH"
        elif risk_score >= 20:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
            
        prediction = "scam" if is_scam else "legitimate"
        
        indicators = []
        if is_scam:
            if risk_score >= 80:
                indicators.append("High scam probability from the ML model")
            else:
                indicators.append("Elevated scam probability from the ML model")
                
            scam_keywords = ['urgent', 'blocked', 'otp', 'verify', 'password', 'bank', 'prize', 'winner', 'click here']
            detected_words = [w for w in scam_keywords if w in message.lower()]
            if detected_words:
                indicators.append(f"Suspicious scam-related keywords detected: {', '.join(detected_words)}")
                
            if 'http' in message.lower() or 'www' in message.lower():
                indicators.append("Message contains a potentially dangerous link")
        else:
            indicators.append("Low scam probability based on the trained model")

        return {
            "prediction": prediction,
            "confidence": round(confidence, 4),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "indicators": indicators
        }

ml_service = MLService()
