# personal_assistant.py
import speech_recognition as sr
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import datetime

class PersonalAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Say something:")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognize_speech(audio)
                print("You said:", text)
                return text
            except sr.UnknownValueError:
                print("Sorry, could not understand audio.")
                return None

    def recognize_speech(self, audio):
        return self.recognizer.recognize_google(audio)

    def process_text(self, text):
        tokens = word_tokenize(text)
        tagged_tokens = pos_tag(tokens)
        lemmatizer = WordNetLemmatizer()

        # Lemmatize words
        lemmatized_tokens = [lemmatizer.lemmatize(word, get_wordnet_pos(tag))
                             for word, tag in tagged_tokens]

        return lemmatized_tokens

    def get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            return "Positive"
        elif sentiment < 0:
            return "Negative"
        else:
            return "Neutral"

    def execute_command(self, command):
        if "time" in command:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"The current time is {current_time}.")
        elif "weather" in command:
            # Implement weather API integration here
            print("Fetching weather information...")
        else:
            print("Command not recognized. Please try again.")

if __name__ == "__main__":
    assistant = PersonalAssistant()

    while True:
        user_input = assistant.listen()

        if user_input:
            processed_input = assistant.process_text(user_input)
            sentiment = assistant.analyze_sentiment(user_input)
            print(f"Sentiment: {sentiment}")

            # Execute command based on processed input
            assistant.execute_command(processed_input)
