from networkSecurity.entity.artifact_enity import DataIngestionArtifacts ,DataValidationArtifacts
from networkSecurity.entity.config_entity import DataValidationConfig
from networkSecurity.exception.NetworkSecurityException import NetworkSecurityException
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networkSecurity.constants.training_pipeline import TARGET_COLUMN , DATA_TRANSFORMATION_IMPUTER_PARAMS
from networkSecurity.entity.artifact_enity import DataTransformationArtifacts ,DataValidationArtifacts
from networkSecurity.entity.config_entity import DataTransformationConfig
from networkSecurity.logging.logger import logging
from networkSecurity.utils.main_utils.utils import save_numpy_array_data , save_object
import pandas as pd
import numpy as np
import sys,os


class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifacts,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifacts = data_validation_artifact
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def get_data_transformer_object(cls)->Pipeline:
        """
        It initialies a KNN imputer obj with the parameters se=pecified in the training_pipeline.py file
        and returns a Pipeline object with KNN imputer object as it first step
        
        Args:
        cls: Data Transformation
        
        Returns:
        A pipleine object
        
        """
        logging.info("Enter data tranformation object (KNN imputer)")
        
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"initalised KNN imputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor:Pipeline = Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
                
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
    
    def initiate_data_transformation(self)->DataTransformationArtifacts:
        logging.info("Enterd initiate_data_transformation method")
        try:
            logging.info("Starting data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            ## training df and test df
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            target_feature_test_df = target_feature_test_df.replace(-1,0)
            
            preprocessor = self.get_data_transformer_object()
            transformed_input_train_feature = preprocessor.fit_transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor.transform(input_feature_test_df)
            
            train_arr = np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]
            
            ## save numpy array
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path , preprocessor)
            
            ## prepare artifacts
            data_transformation_artifacts = DataTransformationArtifacts(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifacts
            
        except Exception  as e:
            raise NetworkSecurityException(e,sys)
        
     