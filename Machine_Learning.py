# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold
from openpyxl import load_workbook
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'Total.xlsx')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
MODEL_FILES = {
    'interlock': os.path.join(MODELS_DIR, 'nn_interlock.joblib'),
    'bottom_thickness': os.path.join(MODELS_DIR, 'nn_bottom_thickness.joblib'),
    'joining_force': os.path.join(MODELS_DIR, 'nn_joining_force.joblib'),
}

FEATURE_COLUMNS = [
    'Rivet Length [mm]',
    'Rivet Inner Diameter [mm]',
    'Die Diameter [mm]',
    'Die Depth [mm]'
]
TARGET_COLUMNS = [
    'Interlock [mm]',
    'Bottom Thickness [mm]',
    'Joining Force [kN]'
]


def load_excel_data(path=DATA_PATH):
    wb = load_workbook(path, read_only=True, data_only=True)
    sheet = wb.active
    rows = list(sheet.values)
    headers = rows[0]

    data_rows = []
    for row in rows[1:]:
        if row is None:
            row_values = [None] * len(headers)
        else:
            row_values = list(row)[:len(headers)]
            if len(row_values) < len(headers):
                row_values += [None] * (len(headers) - len(row_values))
        data_rows.append(row_values)

    df = pd.DataFrame(data_rows, columns=headers)
    df = df.dropna(subset=FEATURE_COLUMNS + TARGET_COLUMNS)
    return df


def build_models():
    df = load_excel_data()
    X = df[FEATURE_COLUMNS].astype(float)
    Y_interlock = df[TARGET_COLUMNS[0]].astype(float)
    Y_bottom = df[TARGET_COLUMNS[1]].astype(float)
    Y_force = df[TARGET_COLUMNS[2]].astype(float)

    nn_interlock = Pipeline([
        ('scaler', StandardScaler()),
        ('mlp', MLPRegressor(
            hidden_layer_sizes=(6,),
            activation='tanh',
            alpha=0.001,
            solver='lbfgs',
            max_iter=5000,
            random_state=100
        ))
    ])
    nn_interlock.fit(X, Y_interlock)

    nn_bottom = Pipeline([
        ('scaler', StandardScaler()),
        ('mlp', MLPRegressor(
            hidden_layer_sizes=(8,),
            activation='tanh',
            alpha=0.0001,
            solver='lbfgs',
            max_iter=5000,
            random_state=100
        ))
    ])
    nn_bottom.fit(X, Y_bottom)

    nn_force = Pipeline([
        ('scaler', StandardScaler()),
        ('mlp', MLPRegressor(
            hidden_layer_sizes=(9,),
            activation='logistic',
            alpha=1.0,
            solver='lbfgs',
            max_iter=5000,
            random_state=100
        ))
    ])
    nn_force.fit(X, Y_force)

    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(nn_interlock, MODEL_FILES['interlock'])
    joblib.dump(nn_bottom, MODEL_FILES['bottom_thickness'])
    joblib.dump(nn_force, MODEL_FILES['joining_force'])

    return nn_interlock, nn_bottom, nn_force


def load_models():
    if all(os.path.exists(path) for path in MODEL_FILES.values()):
        return (
            joblib.load(MODEL_FILES['interlock']),
            joblib.load(MODEL_FILES['bottom_thickness']),
            joblib.load(MODEL_FILES['joining_force'])
        )
    return build_models()


def predict_from_input(models, rivet_length, rivet_inner_diameter, die_diameter, die_depth):
    X_new = np.array([[rivet_length, rivet_inner_diameter, die_diameter, die_depth]], dtype=float)
    interlock_pred = float(models[0].predict(X_new)[0])
    bottom_pred = float(models[1].predict(X_new)[0])
    force_pred = float(models[2].predict(X_new)[0])
    return interlock_pred, bottom_pred, force_pred


if __name__ == '__main__':
    models = build_models()
    print('Modelos treinados e guardados em', MODELS_DIR)

