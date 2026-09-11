from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import re

class URLFeatureExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
        
    def transform(self, X, y=None):
        features = []
        for url in X:
            url_str = str(url)
            length = len(url_str)
            num_digits = sum(c.isdigit() for c in url_str)
            num_dots = url_str.count('.')
            num_hyphens = url_str.count('-')
            num_slashes = url_str.count('/')
            num_at = url_str.count('@')
            has_https = 1 if url_str.startswith('https://') else 0
            has_ip = 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url_str) else 0
            
            # Additional suspicious keywords (binary presence)
            suspicious_words = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'confirm']
            has_suspicious = 1 if any(w in url_str.lower() for w in suspicious_words) else 0
            
            features.append([
                length, num_digits, num_dots, num_hyphens, num_slashes, num_at, has_https, has_ip, has_suspicious
            ])
        return np.array(features)
