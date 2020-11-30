from flask import Flask, request, render_template, jsonify, Response
import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import PorterStemmer
from textblob import TextBlob
from nltk.corpus import wordnet

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

def count_w_numb():
    # calculate the total words you input
    str = request.form['text1']
    # split all the words with space and punctuation mark
    pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
    str1 = re.split(pattern, str)
    lenth = len(str1)
    lenth1 = len(str)   # the length of the inputs
    strr = ["The number of words you have spoken is ", lenth,"The lenth of the inputs is ", lenth1]
    return (strr)


def hyponyms():
    text1 = request.form['text1']
    pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
    str1 = re.split(pattern, text1)
    result = []
    for s in str1:
        syn_set = wordnet.synsets(s)
        for ss in syn_set:
            rere = [s, ss.hyponyms()]
            for rr in rere:
                result.append(rere)
    return (result)


def reverse_input():
    given = request.form['text1']
    givenlen = len(given)
    slicedgiven = str[givenlen::-1]
    return(slicedgiven)


def translate_input():
    blob = TextBlob(request.form['text1'])
    blob.translate(from_lang='en', to= 'zh')
    return(blob)


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

    elif text2 == 'stem':
        combine_6 = sent_stem()
        result = {"output": combine_6}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2 == 'reverse':
        combine_7 = reverse_input()
        result = {"output": combine_7}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2 == 'translate':
        combine_8 = translate_input()
        result = {"output": combine_8}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2 == 'words count':
        combine_9 = count_w_numb()
        result = {"output": combine_9}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2 == 'hyponyms':
        combine_10 = hyponyms()
        result = {"output": combine_10}
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)

    elif text2 == 'ALL':
        text = remove_stop_words() + '\n ' + uppercase_all_words() + '\n ' + word_appearance_count() + '\n ' + POS_tag() + '\n ' + sent_token() + '\n ' + sent_stem() + '\n ' + reverse_input() + '\n ' + count_w_numb() + '\n' + hyponyms() + '\n' + translate_input()
        result = {"output1": remove_stop_words(),
                  "output2": uppercase_all_words(),
                  "output3": word_appearance_count(),
                  "output4": POS_tag(),
                  "output5": sent_token(),
                  "output6": sent_stem(),
                  "output7": reverse_input(),
                  "output8": count_w_numb(),
                  "output9": hyponyms(),
                  "output10": translate_input()
                  }
        result = {str(key): value for key, value in result.items()}
        return jsonify(result=result)
    else:
        print("400 Bad request")
        return jsonify(result="Not Found"), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
