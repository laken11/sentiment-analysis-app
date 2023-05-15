# Emotion Analysis App - How It Works

This is the documentation for the Emotion Analysis App, which analyzes the emotional state of text data. Below are the steps involved in the process:

## Step 1: Data acquisition
Twitter and Reddit, popular social media platforms, were scraped for data based on known stressors and their identifiers. Each stressor scrape generated a dataset of at least 1000 text data entries.

## Step 2: Data processing
The acquired data for each stressor was saved as a CSV file containing a column called "text." Each cell in this dataset was preprocessed to remove unnecessary characters and tokenized. Tokenization is a crucial step in sentiment analysis that involves breaking down the text into individual words or tokens. It helps in analyzing and understanding the text data more effectively by removing punctuation, whitespace, and other irrelevant characters.

## Step 3: Sentiment analysis
Sentiment analysis is performed on the tokenized text to determine the negativity and positivity of the text. The goal is to identify emotional states in the text and classify them into True positive, True negative, False positive, and False negative categories. Texts are classified based on the presence of identified stressors and the level of negativity expressed.

## Step 4: Model training and testing
The models are trained and tested using the categorized datasets. The datasets are divided into training and testing data. After testing, the accuracy scores of the trained models are recorded.

## Step 5: Web application
A web application is developed to enable users to select the identified stressor and input text for analysis. Users can paste the text and request analysis through the web application.

## Step 6: Model classification
The trained models are used for classifying any given text. Users select the identified stressor and input the text on the web page. The text is then analyzed, and the result is displayed to the user.

For more details and code implementation, please refer to the corresponding files in this repository.

---

This documentation provides an overview of how the Emotion Analysis App works. For detailed instructions on installation, setup, and usage, please refer to the [User Manual](link-to-user-manual) or the [Wiki](link-to-wiki) of this repository.

If you have any questions or need further assistance, please feel free to contact our team by [email](mailto:example@example.com).

We hope you find the Emotion Analysis App useful!
