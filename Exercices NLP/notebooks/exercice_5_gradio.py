from transformers import pipeline
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flair.models import TextClassifier
from flair.data import Sentence
import gradio as gr


vader = SentimentIntensityAnalyzer()

classifier = TextClassifier.load('en-sentiment')


def predict_sentiment(text, model_choice):
    try:
        if not text or not text.strip():
            return "Please enter some text."

        if model_choice == "Model 1 (TextBlob)":
            sentiment = TextBlob(text).sentiment
            return (
                f"Polarity: {sentiment.polarity:.4f}\n"
                f"Subjectivity: {sentiment.subjectivity:.4f}"
            )
        
        elif model_choice == "Model 2 (Naive Bayes)":
            sentiment = TextBlob(text, analyzer=NaiveBayesAnalyzer()).sentiment
            return (
                f"Classification : {sentiment.classification}\n"
                f"Positive Probability : {sentiment.p_pos:.4f}\n"
                f"Negative Probability : {sentiment.p_neg:.4f}"
            )
        
        elif model_choice == "Model 3 (VADER)":
            sentiment = vader.polarity_scores(text)
            return (
                f"Score Negative : {sentiment["neg"]:.4f}\n"
                f"Score Neutrel : {sentiment["neu"]:.4f}\n"
                f"Score Positive : {sentiment["pos"]:.4f}\n"
                f"Compound : {sentiment["compound"]:.4f}"
            )
        
        elif model_choice == "Model 4 (Flair)":
            sentence = Sentence(text)
            classifier.predict(sentence)
            score = sentence.labels[0].score
            value = sentence.labels[0].value
            return (
                f"Sentiment : {value}\n"
                f"Score : {score:.4f}"
            )

        return "Unknown model selected."

    except Exception as e:
        return f"Error processing input: {str(e)}"


def documentation():
    return """
## Sentiment Analysis Documentation

Welcome to the Sentiment Analysis Demo!

This application analyzes sentiment using four approaches:

### Models


- **Model 1: TextBlob**
  - Rule/statistics-based sentiment analyzer.
  - Produces:
    - **Polarity** (-1 to 1)
    - **Subjectivity** (0 to 1)

- **Model 2: TextBlob (Naive Bayes)**
  - Machine learning-based analyzer trained on a movie review corpus.
  - Uses a probabilistic classifier to determine sentiment.
  - Produces:
    - **Classification** (pos / neg)
    - **Probability** (0 to 1 for both positive and negative)

- **Model 3: VADER**
  - Lexicon and rule-based sentiment analysis tool specifically attuned to social media style text.
  - Expertly handles emojis, capitalization (e.g., "GREAT"), punctuation (e.g., "!!!"), and slang.
  - Produces:
    - **Positive, Neutral, and Negative scores** (relative proportions)
    - **Compound score** (-1 to 1, a normalized global metric)

- **Model 4: Flair**
  - Advanced deep learning-based sentiment analyzer built on state-of-the-art NLP transformers.
  - Understands context, word order, and subtle linguistic nuances better than rule-based models.
  - Produces:
    - **Value** (POSITIVE / NEGATIVE)
    - **Confidence Score** (0 to 1)


### Data Privacy

Input text is processed only during the current session and is not stored by the application.
"""


with gr.Blocks(title="Sentiment Analysis", theme=gr.themes.Mario()) as demo:
    with gr.Tabs():

        with gr.TabItem("Demo"):
            gr.Markdown(
                """
                ### Sentiment Analysis Demo
                Enter text and choose a model for sentiment analysis.
                """
            )

            with gr.Row():
                with gr.Column(scale=2):
                    text_input = gr.Textbox(
                        label="Input Text",
                        placeholder="Type here or select an example..."
                    )

                    model_choice = gr.Radio(
                        [
                            "Model 1 (TextBlob)",
                            "Model 2 (Naive Bayes)",
                            "Model 3 (VADER)",
                            "Model 4 (Flair)"
                        ],
                        label="Model Choice",
                        value="Model 1 (TextBlob)"
                    )

                    submit_button = gr.Button("Analyze")

                with gr.Column(scale=2):
                    output = gr.Textbox(
                        label="Result",
                        lines=8,
                        max_lines=12,
                        interactive=False
                    )

            gr.Examples(
                examples=[
                    ["I absolutely love this product! It has changed my life."],
                    ["This is the worst movie I have ever seen. Completely disappointing."],
                    ["It's-a me, Mario !"],
                    ["Scrafty is my favorite Pokemon !"],
                    ["Honestly, this was quite a mediocre experience. Nothing special."]
                ],
                inputs=text_input
            )

            submit_button.click(
                fn=predict_sentiment,
                inputs=[text_input, model_choice],
                outputs=output
            )

        with gr.TabItem("Documentation"):
            gr.Markdown(documentation())

demo.launch()