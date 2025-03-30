from networkSecurity.entity.artifact_enity import DataIngestionArtifacts ,DataValidationArtifacts
from networkSecurity.entity.config_entity import DataValidationConfig
from networkSecurity.exception.NetworkSecurityException import NetworkSecurityException
from networkSecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networkSecurity.logging.logger import logging
from networkSecurity.utils.main_utils.utils import read_yaml_file , write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import sys,os


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifacts, data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self.schema_config)
            logging.info(f"Required number of columns :{number_of_columns}")
            logging.info(f"DataFrame has columns :{len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_dataset_drift(self, base_df , current_df , threshold =0.5)->bool:
        try:
            status = True
            report= {}
            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]
                isn_same_dist=ks_2samp(d1,d2)
                if threshold<=isn_same_dist.pvalue:
                    is_found =False
                else:
                    is_found = True 
                    status =False
                report.update({col:{"p_value":float(isn_same_dist.pvalue),"drift_staus":is_found}})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            # create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)            
        except Exception as e:
            raise NetworkSecurityException(e,sys)            

    
    def initiate_data_validation(self)->DataValidationArtifacts:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            ## read the data from train and test
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            
            ## Validate no. of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message =f"Train dataframe doesnt contain all columns \n"
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message =f" Test dataframe doesnt contain all columns \n" 
            
            ## lets check  datadrift 
            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
            )      
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path , index= False,header = True
            )
            
            data_validation_artifacts= DataValidationArtifacts(
                validation_status= status,
                valid_train_file_path= self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path= self.data_ingestion_artifact.test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifacts   
        except Exception as e:
            raise NetworkSecurityException(e,sys)


