import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.predict import VisaPredictor

_predictor_instance = None

def get_model_service():
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = VisaPredictor()
    return _predictor_instance
