from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.exception.NetworkSecurityException import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.config_entity import DataIngestionConfig
from networkSecurity.entity.config_entity import TrainingPipelineConfig
import sys
import os

if __name__ == '__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig =DataIngestionConfig(trainingpipelineconfig)
        dataingestion = DataIngestion(dataingestionconfig)
        logging.info("Initate the data ingestion")
        data_artifact=dataingestion.initiate_data_ingestion()
        print(data_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)    
        