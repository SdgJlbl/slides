import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import joblib


def standardise_data(input_file):
    df = pd.read_csv(input_file, index_col=0)
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(columns="label"),
        df["label"],
        stratify=df["label"],
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    parameters = pd.DataFrame(
        data=np.vstack((scaler.mean_, scaler.scale_)),
        columns=scaler.feature_names_in_,
        index=["mean", "scale"],
    )
    parameters.to_csv("standardisation_parameters.csv")
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test


def train_classifier(cleaned_data, labels, model_name):
    classifier = LogisticRegression()
    classifier.fit(cleaned_data, labels)
    joblib.dump(classifier, model_name)


def evaluate(model, data, label):
    classifier = joblib.load(model)
    return confusion_matrix(label, classifier.predict(data))


def main():
    X_train, X_test, y_train, y_test = standardise_data("input.csv")
    model_name = "saved_model.pkl"
    train_classifier(X_train, y_train, model_name)
    print(evaluate(model_name, X_test, y_test))
