import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
import joblib


def standardise_data(input_file):
    df = pd.read_csv(input_file, index_col=0)
    X_train = df.drop(columns="label")
    y_train = df["label"]

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    parameters = pd.DataFrame(
        data=np.vstack((scaler.mean_, scaler.scale_)),
        columns=scaler.feature_names_in_,
        index=["mean", "scale"],
    )
    parameters.to_csv("standardisation_parameters.csv")
    return X_train_scaled, y_train


def train_classifier(cleaned_data, labels, model_name):
    classifier = LogisticRegression()
    classifier.fit(cleaned_data, labels)
    joblib.dump(classifier, model_name)


def evaluate(model, input_file):
    classifier = joblib.load(model)
    df = pd.read_csv(input_file, index_col=0)
    X = df.drop(columns="label")
    y = df["label"]
    return confusion_matrix(y, classifier.predict(X))


def main():
    X_train, y_train = standardise_data("trainset.csv")
    train_classifier(X_train, y_train, "saved_model.pkl")
    print(evaluate("saved_model.pkl", "testset.csv"))
