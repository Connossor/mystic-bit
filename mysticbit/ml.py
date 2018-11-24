""" Core ML functions"""
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import LeavePGroupsOut


def train_test_split(df_ml):
    """ Split log data into train and test by well ID """

    test_wells = set(['B03', 'B05', 'B06'])
    train_wells = set(df_ml.HACKANAME.unique()) - test_wells
    print('Train well: ', train_wells)
    print('Test wells: ', test_wells)

    mask_train = df_ml.HACKANAME.isin(train_wells)
    df_ml_train = df_ml[mask_train]
    df_ml_test = df_ml[~mask_train]

    return df_ml_train, df_ml_test


def make_model(df_ml_train, X_cols, y_cols):
    """ Returns a trained model """

    X_train = df_ml_train[X_cols]
    y_train = df_ml_train[y_cols]

    model = MultiOutputRegressor(RandomForestRegressor())
    model.fit(X_train, y_train)
    return model


def make_predictions(model, df_ml, X_cols, y_cols):
    df_pred = df_ml.copy()
    """ Use trained model to make predictions, add on to df_ml as new column"""

    X = df_pred[X_cols]
    y = df_pred[y_cols]

    y_pred = model.predict(X)
    pred_cols = [c + '_pred' for c in y_cols]
    df_pred[pred_cols] = pd.DataFrame(y_pred, index=df_pred.index)
    return df_pred
