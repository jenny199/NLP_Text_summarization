from  flask import Flask, render_template, request
import joblib
import re
from model import TextSummarize
import math

app = Flask(__name__)
def preprocessing(text):
  article_text = re.sub(r'\[[0-9]*\]', ' ', text)
  article_text = re.sub(r'\s+', ' ', article_text)
  article_text=article_text.replace("\"", "")
  return article_text
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def predict():

    text = request.form.get('text')
    # textfile = request.files['textfile']
    # text_path = "./text" + textfile.filename
    # textfile.save(text_path)
    # text = open(text_path,"r")
    # article_text = text.read()
    summary = preprocessDataAndSummarize(text)
    

    return render_template('index.html', input = text, prediction = summary)

@app.route('/summarizeUploaded', methods=['POST'])
def predictupload():

    # text = request.form.get('text')
    textfile = request.files['textfile']
    text_path = "./text" + textfile.filename
    textfile.save(text_path)
    text = open(text_path,"r")
    article_text = text.read()

    #calling a preprocessing function
    article_text = preprocessing(article_text)
    
    #calling a text summarizer model
    textsummary = TextSummarize(article_text, threshold=0.01,ratio=0.5)
    summary = textsummary.summary
    

    return render_template('index.html', input = article_text, prediction = summary)

def preprocessDataAndSummarize(text):

    #preprocess by removing extra spaces and /\ in the middle of sentences
    article_text = re.sub(r'\[[0-9]*\]', ' ', text)
    article_text = re.sub(r'\s+', ' ', article_text)
    article_text=article_text.replace("\"", "")

    #open file
    # file_model = open('./saved_models/text_summarizer.pkl', "rb")

    #load file
    textsummary = TextSummarize(article_text, threshold=0.01,ratio=0.5)
    summary = textsummary.summary
    return summary







if __name__ == '__main__':
    app.run(debug=True)