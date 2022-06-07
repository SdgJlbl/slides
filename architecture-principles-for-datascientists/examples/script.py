import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix

df_train = pd.read_csv("trainset.csv", index_col=0)
df_test = pd.read_csv("testset.csv", index_col=0)
X_train = df_train.drop(columns="label")
X_test = df_test.drop(columns="label")
y_train = df_train["label"]
y_test = df_test["label"]

# standardize the date to avoid badly conditioned matrices
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# train a logistic regression classifier
classifier = LogisticRegression()
classifier.fit(X_train_scaled, y_train)

# apply the result to test data
X_test_scaled = scaler.transform(X_test)
confusion_matrix(y_test, classifier.predict(X_test_scaled))
