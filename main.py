from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.components.data_validation import DataValidation, DataValidationConfig
from networkSecurity.components.data_tranformation import DataTransformationConfig ,DataTransformation
from networkSecurity.exception.NetworkSecurityException import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.config_entity import DataIngestionConfig
from networkSecurity.entity.config_entity import TrainingPipelineConfig
from networkSecurity.components.model_trainer import ModelTrainerArtifacts ,ModelTrainer ,ModelTrainerConfig
import sys
import os

if __name__ == '__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig =DataIngestionConfig(trainingpipelineconfig)
        dataingestion = DataIngestion(dataingestionconfig)
        logging.info("Initate the data ingestion")
        data_artifact=dataingestion.initiate_data_ingestion()
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(data_artifact,data_validation_config=data_validation_config)
        logging.info("Initate the data Validation")
        data_validation_artifacts=data_validation.initiate_data_validation()
        logging.info("data validation completed")
        print(data_validation_artifacts)
        data_tranformation_config = DataTransformationConfig(trainingpipelineconfig)
        data_transforamtion = DataTransformation(data_validation_artifacts,data_tranformation_config)
        data_transformation_artifacts = data_transforamtion.initiate_data_transformation()
        logging.info("data transformation started")
        print(data_transformation_artifacts)
        logging.info("data transformation completed")
        logging.info("Model training started")
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config,data_transformation_artifacts)
        model_trainer_artifacts = model_trainer.initiate_model_trainer()
        logging.info("Model training completed")
    except Exception as e:
        raise NetworkSecurityException(e,sys)    
        