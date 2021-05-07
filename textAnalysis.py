import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Takes a string and filters out stopwords and punctuation.
def clean_text_data(text):

    tokenized_text = word_tokenize(text)
    filtered_text = []
    stop_words = set(stopwords.words("english"))
    punctuation = {'.', ',', '?', '!', '"', '|', '[', ']', '{', '}', '/', '-', '...'}
    for word in tokenized_text:
        if word not in stop_words and word not in punctuation:
            filtered_text.append(word)
    return " ".join(filtered_text)

# Takes a string and returns the polarity (sentiment) score for it
def evaluateSentiments(text):
    sia = SentimentIntensityAnalyzer()
    review = text.split(" ")
    polarity_total = 0
    for word in review:
        score = sia.polarity_scores(word)['compound']
        polarity_total += score
    return polarity_total


def main():
    cleaned_text = clean_text_data("hello? I love pie!!")
    score = evaluateSentiments(cleaned_text)
    print(score)

if __name__ == "__main__":
    main()
