import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.explain import VisaExplainer

_explainer_instance = None

def get_explanation_service():
    global _explainer_instance
    if _explainer_instance is None:
        _explainer_instance = VisaExplainer()
    return _explainer_instance
