import glob
import spacy
nlp=spacy.blank("en")
nlp=spacy.load('en_core_web_sm')
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import re
import os
from spacy.util import filter_spans
import nltk
#nltk.download('wordnet')
from nltk.corpus import wordnet
from nltk.tokenize  import sent_tokenize,word_tokenize
from commonregex import CommonRegex

def inputfiles(file):
    with open(file, 'r') as f:
        document = f.read()
    return document

def names(doc):
    nlp_doc=nlp(doc)
    names_list=[]
    pattern = [{'POS': 'PROPN'},{'ORTH': ',', 'OP': '?'}, {'POS':'PROPN','OP':'?'}]
    matcher=Matcher(nlp.vocab)
    matcher.add('FULL_NAME', [pattern])
    matches = matcher(nlp_doc)
    for match_id, start, end in matches:
        span = nlp_doc[start:end]
        for i in span.ents:
            if i.label_=='PERSON':
                names_list.append(i.text)
    names_list.sort(reverse=True)
    for i in names_list:
        doc=doc.replace(i,u"\u2588" * len(i))
    nlp_doc1 = nlp(doc)
    for word in nlp_doc1.ents:
        if word.label_ == "PERSON":
            names_list.append(word.text)
    names_list.sort(reverse=True)
    for i in names_list:
        doc = doc.replace(i, u"\u2588" * len(i))
    return doc, names_list

def dates(doc):
    dates_list = []
    doc1 = CommonRegex(doc)
    if doc1.dates != 0:
        for d in doc1.dates:
            dates_list.append(d)
    for i in dates_list:
        doc = doc.replace(i, u"\u2588" * len(i))
    return doc, dates_list

def phone_numbers(doc):
    phone_list = []
    doc1 = CommonRegex(doc)
    if doc1.phones != 0:
        for n in doc1.phones:
            count = 0
            for i in range(0, len(n)):
                if n[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    count += 1
                elif n[i] == '.':
                    break
            if count == 10 or count == 11:
                phone_list.append(n)
    for i in phone_list:
        doc = doc.replace(i, u"\u2588" * len(i))
    return doc, phone_list

def gender(doc):
    nlp_doc=nlp(doc)
    g_list=['she', 'he', 'her', 'him', 'his', 'father', 'mother', 'male', 'female', 'daughter', 'son', 'sons', 'lady', 'gentlemen',
            'grandma', 'grandpa', 'dad', 'mom', 'uncle', 'aunt', 'sister', 'sisters', 'ms', 'mr', 'mrs', 'husband', 'wife', 'wives', 'herself',
            'himself', 'guy', 'grandfather', 'grandmother', 'boyfriend', 'boyfriends', 'girlfriend', 'girlfriends', 'grandson',
           'granddaughter', 'groom', 'bride', 'king', 'queen', 'nephew', 'nephews', 'niece', 'nieces', 'uncles', 'fiancee', 'goddess', 'ladies'
            'princess', 'waiter', 'widower', 'widowers', 'waiter', 'waitress', 'widow', 'widows', 'woman', 'man', 'men', 'women', 'woman',
            'moms', 'guy', 'guys', 'dude', 'folk', 'folks', 'gay', 'lesbian', 'parent', 'parents', 'child', 'children', 'spouse', 'server',
            'mankind', 'fireman', 'freshman', 'chairman', 'mailman', 'policeman', 'cop', 'salesman', 'saleswoman', 'student', 'students',
            'doctor', 'nurse', 'patient', 'professor', 'professors', 'brother', 'brothers', 'siblings', 'priest', 'priests', 'poet', 'governor',
            'infant', 'baby', 'toodler', 'toodlers', 'transgender']
    gender_list=[]
    for i in nlp_doc:
        if i.pos_=='PRON':
            if i.text.lower() in g_list:
                gender_list.append(i.text)
        elif i.text.lower() in g_list:
            gender_list.append(i.text)
    for i in gender_list:
        doc=doc.replace(i,u"\u2588" * len(i))
    return doc, gender_list

def address(doc):
    nlp_doc=nlp(doc)
    address_list=[]
    pattern=[{'POS':'NUM'},{'POS':'PROPN'},{'POS':'PROPN'},{'POS':'PROPN'},{'POS':'PUNCT'},{'POS':'PROPN'}]
    matcher=Matcher(nlp.vocab)
    matcher.add('ADDRESS',[pattern])
    matches=matcher(nlp_doc)
    for match_id, start, end in matches:
        span=nlp_doc[start:end]
        address_list.append(span.text)
    for i in nlp_doc.ents:
        if i.label_=='GPE':
            address_list.append(i.text)
    for i in address_list:
        doc=doc.replace(i,u"\u2588" * len(i))
    return doc,address_list

def concept(doc, w):
    nlp_doc=nlp(doc)
    synonyms=[]
    synonyms_list=[]
    sentences_list=[]
    for synset in wordnet.synsets(w):
        for lemma in synset.lemmas():
            synonyms.append(lemma.name())
    synonyms_list = set(synonyms)
    sentences = nltk.sent_tokenize(doc)
    for sentence in sentences:
        for c in synonyms_list:
            if c.lower() in sentence.lower():
                sentences_list.append(sentence)
                doc = doc.replace(sentence, u"\u2588" * len(sentence))
    return doc,sentences_list

def output(doc,filename,path):
    directory=path
    output_path = os.path.join(os.getcwd(), directory)
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as error:
        print("ERROR")
    outputfile=('%s/%s.redacted' %(output_path, filename))
    with open(outputfile, "w+", encoding='utf-8') as f:
        f.write(doc)
        f.close()

stats_list=[]
def stats(doc_stats,stats_path,filename,w):
    nlp_doc=nlp(doc_stats)
    stats=''
    (doc_stats,names_redacted)=names(doc_stats)
    stats="The number of names redacted from %s is: %d" %(filename, len(names_redacted)) + '\n'
    stats_list.append(stats)
    (doc_stats,dates_redacted)=dates(doc_stats)
    stats="The number of dates redacted from %s is: %d" %(filename, len(dates_redacted)) + '\n'
    stats_list.append(stats)
    (doc_stats,phone_redacted)=phone_numbers(doc_stats)
    stats="The number of phone numbers redacted from %s is: %d" %(filename, len(phone_redacted)) +'\n'
    stats_list.append(stats)
    (doc_stats,gender_redacted)=gender(doc_stats)
    stats="The number of gender terms redacted from %s is: %d" %(filename, len(gender_redacted)) +'\n'
    stats_list.append(stats)
    (doc_stats,address_redacted)=address(doc_stats)
    stats="The number of addresses redacted from %s is: %d" %(filename, len(address_redacted)) +'\n'
    stats_list.append(stats)
    (doc_stats,sentences_redacted)=concept(doc_stats,w)
    stats="The number of sentences redacted from %s is: %d" %(filename, len(sentences_redacted)) +'\n'+'\n'
    stats_list.append(stats)

    if stats_path=='stdout':
        for i in stats_list:
            print(i)
    else:
        with open(stats_path, 'w') as f:
            for i in stats_list:
               f.write(i)
            f.close()
