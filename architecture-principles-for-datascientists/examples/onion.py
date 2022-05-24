import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import joblib


def standardise_data(X_train):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    parameters = pd.DataFrame(
        data=np.vstack((scaler.mean_, scaler.scale_)),
        columns=scaler.feature_names_in_,
        index=["mean", "scale"],
    )
    return X_train_scaled, parameters


def train_classifier(cleaned_data, labels):
    classifier = LogisticRegression()
    classifier.fit(cleaned_data, labels)
    return classifier


def evaluate(scaler, classifier, data, label):
    cleaned_data = scaler.transform(data)
    return confusion_matrix(label, classifier.predict(cleaned_data))


def load_scaler(parameters_file):
    parameters = pd.read_csv(parameters_file, index_col=0)
    scaler = StandardScaler()
    scaler.scale_ = parameters.loc["scale"].values
    scaler.mean_ = parameters.loc["mean"].values
    scaler.feature_names_in_ = list(parameters.columns)
    return scaler


def main():
    input_file = "input.csv"
    preprocess_file = "scaler.csv"
    model_name = "saved_model.pkl"
    df = pd.read_csv(input_file, index_col=0)
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(columns="label"),
        df["label"],
        stratify=df["label"],
    )
    # preprocessing
    X_train_cleaned, scaling_parameters = standardise_data(X_train)
    scaling_parameters.to_csv(preprocess_file)

    #training
    model = train_classifier(X_train_cleaned, y_train)
    joblib.dump(model, model_name)

    # evaluating
    scaler = load_scaler(preprocess_file)
    print(evaluate(scaler, model_name, X_test, y_test))
