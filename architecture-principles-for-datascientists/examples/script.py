import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

df = pd.read_csv("input.csv", index_col=0)
X_train, X_test, y_train, y_test = train_test_split(
    df.drop(columns="label"), df["label"], stratify=df["label"]
)

# standardize the date to avoid badly conditioned matrices
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# train a logistic regression classifier
classifier = LogisticRegression()
classifier.fit(X_train_scaled, y_train)

# apply the result to test data
X_test_scaled = scaler.transform(X_test)
confusion_matrix(y_test, classifier.predict(X_test_scaled))
