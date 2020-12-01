from flask import Flask, request, render_template, jsonify, Response
import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer as WL
from textblob import TextBlob
from nltk.corpus import wordnet
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
from nltk import chunk

app = Flask(__name__)


def remove_stop_words():
    input_text = request.form['text1']
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(input_text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    remove_punctuation = []
    for i in filtered_sentence:
        if i not in string.punctuation:
            remove_punctuation.append(i)
        else:
            continue
    result = " ".join(remove_punctuation)
    return result


def uppercase_all_words():
    input_text = request.form['text1']
    return input_text.upper()


def word_appearance_count():
    input_text = request.form['text1']
    counts = dict()
    words = input_text.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return str(counts)


def POS_tag():
    input_text = request.form['text1']
    pre_processing = word_tokenize(input_text)
    tagged = nltk.pos_tag(pre_processing)
    return str(tagged)


def sent_token():
    input_text = request.form['text1']
    sentence = sent_tokenize(input_text,'english')
    return(sentence)

def sent_stem():
    input_text = request.form['text1']
    pre_processing = word_tokenize(input_text,'english')
    stemmer = PorterStemmer()
    stem = list()
    for i in range(len(pre_processing)):
        stem.append(stemmer.stem(pre_processing[i]))
    return(stem)

def long_word_def():
    text1 = request.form['text1']
    pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
    str1 = re.split(pattern, text1)
    long_word = "a"
    for w in str1:
        if len(w) >= len(long_word):
            long_word = w
    syn = wordnet.synsets(long_word)
    meaning = syn[0].definition()
    result = [long_word,meaning]
    return(result)


def sentiment_analysis():
    text1 = request.form['text1']
    sentences = tokenize.sent_tokenize(text1)
    sid = SentimentIntensityAnalyzer()
    score = []
    for sen in sentences:
        s = sid.polarity_scores(sen)
        score.append(s)
    return(score)


def sent_lemma():
    words = request.form['text1']
    wl = WL()
    lemma = wl.lemmatize(words)
    return(lemma)

def translate_input():
    input = request.form['text1']
    blob = TextBlob(input)
    result_1 = blob.translate(from_lang='en', to= 'zh')
    return str(result_1)

def gram_tree():
    input = request.form['text1']
    pre_processing = word_tokenize(input)
    tagged = nltk.pos_tag(pre_processing)
    tree = chunk.ne_chunk(tagged)
    return(tree)

@app.route('/')
def home():
    return render_template('request.html')


@app.route('/join', methods=['GET', 'POST'])
def my_form_post():
    text2 = request.form['text2']
    if text2.lower() == 'stop words':
        combine = remove_stop_words()
        result = {"output": combine}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2.lower() == 'uppercase':
        combine_2 = uppercase_all_words()
        result = {"output": combine_2}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2.lower() == 'appearance count':
        combine_3 = word_appearance_count()
        result = {"output": combine_3}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2.lower() == 'pos_tag':
        combine_4 = POS_tag()
        result = {"output": combine_4}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2.lower() == 'sentence tokenize':
        combine_5 = sent_token()
        result = {"output": combine_5}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2.lower() == 'stem':
        combine_6 = sent_stem()
        result = {"output": combine_6}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2.lower() == 'lemma':
        combine_7 = sent_lemma()
        result = {"output": combine_7}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2.lower() == 'translate':
        combine_8 = translate_input()
        result = {"output": combine_8}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2.lower() == 'longest word definition':
        combine_9 = long_word_def()
        result = {"output": combine_9}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2.lower() == 'sentiment analysis':
        combine_10 = sentiment_analysis()
        result = {"output": combine_10}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2.lower() == 'tree':
        combine_11 = gram_tree()
        result = {"output": combine_11}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2.lower() == 'all':
        #text = remove_stop_words() + '\n ' + uppercase_all_words() + '\n ' + word_appearance_count() + '\n ' + POS_tag() + '\n ' + sent_token() + '\n ' + sent_stem() + '\n '+ sent_lemma() + '\n '  + long_word_def() + '\n' + sentiment_analysis() + '\n' + translate_input() + '\n' + gram_tree()
        result = {"output1": remove_stop_words(),
                  "output2": uppercase_all_words(),
                  "output3": word_appearance_count(),
                  "output4": POS_tag(),
                  "output5": sent_token(),
                  "output6": sent_stem(),
                  "output7": sent_lemma(),
                  "output8": long_word_def(),
                  "output9": sentiment_analysis(),
                  "output10": translate_input(),
                  "output11": gram_tree()
                  }
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)
    else:
        print("400 Bad request")
        return jsonify(result="Not Found"), 400



if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=7000)
    app.run()
