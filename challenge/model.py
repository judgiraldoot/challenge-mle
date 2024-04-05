import os
from datetime import datetime 
from typing import Tuple, Union, List

import xgboost as xgb
import pandas as pd
import numpy as np
class DelayModel:
    """
    A class to represent a model for predicting flight delays.

    Attributes:
        _model (xgb.XGBClassifier): XGBoost classifier model for delay prediction.
    """

    def __init__(self):
        """Initialize the DelayModel class."""
        self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight=4.44) 

    @staticmethod
    def is_high_season(fecha):
        """
        Check if the date corresponds to a high season period.

        Args:
            fecha (str): Date in the format '%Y-%m-%d %H:%M:%S'.

        Returns:
            int: 1 if it's a high season, 0 otherwise.
        """
        fecha_año = int(fecha.split('-')[0])
        fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        range1_min = datetime.strptime('15-Dec', '%d-%b').replace(year = fecha_año)
        range1_max = datetime.strptime('31-Dec', '%d-%b').replace(year = fecha_año)
        range2_min = datetime.strptime('1-Jan', '%d-%b').replace(year = fecha_año)
        range2_max = datetime.strptime('3-Mar', '%d-%b').replace(year = fecha_año)
        range3_min = datetime.strptime('15-Jul', '%d-%b').replace(year = fecha_año)
        range3_max = datetime.strptime('31-Jul', '%d-%b').replace(year = fecha_año)
        range4_min = datetime.strptime('11-Sep', '%d-%b').replace(year = fecha_año)
        range4_max = datetime.strptime('30-Sep', '%d-%b').replace(year = fecha_año)
        
        if ((fecha >= range1_min and fecha <= range1_max) or 
            (fecha >= range2_min and fecha <= range2_max) or 
            (fecha >= range3_min and fecha <= range3_max) or
            (fecha >= range4_min and fecha <= range4_max)):
            return 1
        else:
            return 0

    @staticmethod
    def get_min_diff(data: pd.DataFrame):
        """
        Calculate the difference in minutes between two dates.

        Args:
            data (pd.DataFrame): DataFrame containing 'Fecha-O' and 'Fecha-I' columns.

        Returns:
            float: Difference in minutes between 'Fecha-O' and 'Fecha-I'.
        """
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        min_diff = ((fecha_o - fecha_i).total_seconds())/60
        return min_diff
    
    @staticmethod
    def get_period_day(date):
        """
        Determine the period of the day based on the given time.

        Args:
            date (str): Time in the format '%Y-%m-%d %H:%M:%S'.

        Returns:
            str: Period of the day ('morning', 'afternoon', or 'night').
        """
        date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
        morning_min = datetime.strptime("05:00", '%H:%M').time()
        morning_max = datetime.strptime("11:59", '%H:%M').time()
        afternoon_min = datetime.strptime("12:00", '%H:%M').time()
        afternoon_max = datetime.strptime("18:59", '%H:%M').time()
        evening_min = datetime.strptime("19:00", '%H:%M').time()
        evening_max = datetime.strptime("23:59", '%H:%M').time()
        night_min = datetime.strptime("00:00", '%H:%M').time()
        night_max = datetime.strptime("4:59", '%H:%M').time()
        
        if(date_time > morning_min and date_time < morning_max):
            return 'mañana'
        elif(date_time > afternoon_min and date_time < afternoon_max):
            return 'tarde'
        elif(
            (date_time > evening_min and date_time < evening_max) or
            (date_time > night_min and date_time < night_max)
        ):
            return 'noche'

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        if target_column == 'high_season':
            y = data['Fecha-I'].apply(DelayModel.is_high_season).to_frame(name='high_season')
        elif target_column == "min_diff":
            y = data.apply(DelayModel.get_min_diff, axis = 1).to_frame(name='min_diff')
        elif target_column == 'period_day':
            y = data['Fecha-I'].apply(DelayModel.get_period_day).to_frame(name='period_day')
        elif target_column == 'delay':
            threshold_in_minutes = 15
            yy = data.apply(DelayModel.get_min_diff, axis = 1).to_frame(name='min_diff')
            y = pd.DataFrame(np.where(yy['min_diff'] > threshold_in_minutes, 1, 0), columns=['delay'])
        else:
            y = None

        top_10_features = [
            "OPERA_Latin American Wings", 
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]

        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix = 'OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix = 'TIPOVUELO'), 
            pd.get_dummies(data['MES'], prefix = 'MES')], 
            axis = 1
        )

        registers = data.shape[0]
        num_columns = len(top_10_features)
        zeros_array = [[False] * num_columns] * registers

        X = pd.DataFrame(zeros_array, columns=top_10_features)

        for feature in top_10_features:
            for i in list(range(0, registers)):
                if feature in features.columns:
                    if features[feature][i]:
                        X[feature][i] = True

        if target_column:
            return X, y
        else:
            return X

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """

        self._model.fit(features, target)
        self._model.save_model("delay_model.model")

        return

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, "delay_model.model")
        self._model.load_model(model_path)

        targets_array = self._model.predict(features)
        targets_list = targets_array.tolist()
        targets = [int(element) for element in targets_list]

        return targets