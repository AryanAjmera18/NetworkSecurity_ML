from networkSecurity.exception.NetworkSecurityException import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.artifact_enity import ClassificationMetricArtifacts
from networkSecurity.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import os , sys

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preproccesor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x):
        try:
            x_trasnform = self.preproccesor.trasnform(x)
            y_hat = self.model.predict(x_trasnform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
            