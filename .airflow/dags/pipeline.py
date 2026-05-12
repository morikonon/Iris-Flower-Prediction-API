from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def load_data(**context):
    from sklearn.datasets import load_iris

    iris = load_iris()

    data = {
        "X": iris.data.tolist(),
        "y": iris.target.tolist()
    }

    context["ti"].xcom_push(key="raw_data", value=data)


def split_data(**context):
    from sklearn.model_selection import train_test_split
    import numpy as np

    data = context["ti"].xcom_pull(key="raw_data", task_ids="load_data")

    X = np.array(data["X"])
    y = np.array(data["y"])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    split = {
        "X_train": X_train.tolist(),
        "X_test": X_test.tolist(),
        "y_train": y_train.tolist(),
        "y_test": y_test.tolist(),
    }

    context["ti"].xcom_push(key="split_data", value=split)


def train_model(**context):
    from sklearn.linear_model import LogisticRegression
    import numpy as np
    import pickle
    import base64

    split = context["ti"].xcom_pull(key="split_data", task_ids="split_data")

    X_train = np.array(split["X_train"])
    y_train = np.array(split["y_train"])

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    model_bytes = pickle.dumps(model)
    model_b64 = base64.b64encode(model_bytes).decode("utf-8")

    context["ti"].xcom_push(key="model", value=model_b64)


def evaluate(**context):
    from sklearn.metrics import accuracy_score, f1_score
    import numpy as np
    import pickle
    import base64

    model_b64 = context["ti"].xcom_pull(key="model", task_ids="train_model")
    model = pickle.loads(base64.b64decode(model_b64))

    split = context["ti"].xcom_pull(key="split_data", task_ids="split_data")

    X_test = np.array(split["X_test"])
    y_test = np.array(split["y_test"])

    preds = model.predict(X_test)

    accuracy = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, average="macro")

    print(f"accuracy: {accuracy}")
    print(f"f1_score: {f1}")


with DAG(
    dag_id="logistic_regression",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
    )

    t2 = PythonOperator(
        task_id="split_data",
        python_callable=split_data,
    )

    t3 = PythonOperator(
        task_id="train_model",
        python_callable=train_model,
    )

    t4 = PythonOperator(
        task_id="evaluate",
        python_callable=evaluate,
    )

    t1 >> t2 >> t3 >> t4
