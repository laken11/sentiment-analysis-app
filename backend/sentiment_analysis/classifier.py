from textblob.classifiers import NaiveBayesClassifier
import pandas as pd
import pickle


def train_and_test(data_set_file: str):
    try:
        file_name = f"../scrapping/twitter_data/{data_set_file}.csv"
        df = pd.read_csv(file_name, header=None, names=["text", "label"],
                         skiprows=1)
        df.fillna("", inplace=True)

        # Split the data into training and testing sets
        train_ratio = 0.8  # Percentage of data for training
        train_size = int(len(df) * train_ratio)

        train_df = df[:train_size]
        test_df = df[train_size:]

        _train(train_df, data_set_file)
        _test(test_df, data_set_file)

    except FileNotFoundError as ex:
        print(str(ex))


def _train(train_df: pd.DataFrame, model: str):
    # Convert the training and testing sets to lists
    train = list(train_df.itertuples(index=False, name=None))
    classifier = NaiveBayesClassifier(train)
    _save_model(classifier, model)


def _test(test_df: pd.DataFrame, model: str):
    test = list(test_df.itertuples(index=False, name=None))
    classifier: NaiveBayesClassifier = _load_model(model)
    accuracy = classifier.accuracy(test)
    with open(f"accuracy.txt", "a") as file:
        file.write(f"{model} accuracy score is: {accuracy}\n")
        file.write("--------------------------------------")


def _save_model(classifier: NaiveBayesClassifier, model: str):
    # Save the trained model to a file
    with open(f"{model}.pkl", "wb") as file:
        pickle.dump(classifier, file)


def _load_model(model: str):
    # Load the trained model from the file
    with open(f"{model}.pkl", "rb") as file:
        return pickle.load(file)


def classify(stressor: str, statement: str):
    data_set_file: str = stressor
    classifier: NaiveBayesClassifier = _load_model(data_set_file)
    return classifier.classify(statement)


train_and_test("Ptsd")
