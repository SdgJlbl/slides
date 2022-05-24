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


def main():
    X_train, X_test, y_train, y_test = standardise_data("input.csv")
    model_name = "saved_model.pkl"
    train_classifier(X_train, y_train, model_name)
    print(evaluate(model_name, X_test, y_test))
