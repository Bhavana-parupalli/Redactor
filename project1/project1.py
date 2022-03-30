import glob
import spacy
nlp=spacy.blank("en")
nlp=spacy.load('en_core_web_sm')
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import re
import os
from spacy.util import filter_spans

def inputfiles(file):
    with open(file, 'r') as f:
        document = f.read()
    return document

def names(doc):
    nlp_doc=nlp(doc)
    names_list=[]
    pattern = [{'POS': 'PROPN'},{'POS':'PROPN','OP':'?'}]
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
    return doc,names_list

def dates(doc):
    nlp_doc=nlp(doc)
    l = []
    l1 = []
    dates_list = []
    exp1 = re.findall(r"\d+/\d+/\d\d\d\d", doc)
    for i in exp1:
        dates_list.append(i)
    pattern3 = [{'POS': 'NUM'}, {'POS': 'PROPN'}, {'POS': 'NUM'}]
    matcher = Matcher(nlp.vocab)
    matcher.add('DATE', [pattern3])
    matches = matcher(nlp_doc)
    for match_id, start, end in matches:
        span = nlp_doc[start:end]
        l.append(span)
    l1.append(l)
    for i in l1:
        for j in i:
            if len(j) == 3:
                dates_list.append(j.text)
    for i in dates_list:
        doc = doc.replace(i, u"\u2588" * len(i))
    return doc,dates_list

def phone_numbers(doc):
    nlp_doc=nlp(doc)
    phone_list = []
    pattern = [{'ORTH': '('}, {'SHAPE': 'ddd'},
               {'ORTH': ')'}, {'SHAPE': 'ddd'},
               {'ORTH': '-', 'OP': '?'}, {'SHAPE': 'dddd'}]
    matcher = Matcher(nlp.vocab)
    matcher.add('PHONE_NUMBER', [pattern])
    matches = matcher(nlp_doc)
    for match_id, start, end in matches:
        span = nlp_doc[start:end]
        phone_list.append(span.text)
    for i in phone_list:
        doc = doc.replace(i, u"\u2588" * len(i))
    return doc,phone_list

def gender(doc):
    nlp_doc=nlp(doc)
    g_list=['She', 'he', 'her', 'she', 'him', 'He', 'his', 'father', 'Mother', 'Father', 'mother', 'male', 'female', 'Male', 'Female']
    gender_list=[]
    for i in nlp_doc:
        if i.pos_=='PRON':
            if i.text in g_list:
                gender_list.append(i.text)
        elif i.text in g_list:
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
    sentences_list = []
    phrase_matcher = PhraseMatcher(nlp.vocab)
    phrases = [w, 'Internet','online network']
    patterns = [nlp(text) for text in phrases]
    phrase_matcher.add('CAH', [*patterns])

    for sent in nlp_doc.sents:
        for match_id, start, end in phrase_matcher(nlp(sent.text)):
            if nlp.vocab.strings[match_id] in ['CAH']:
                sentences_list.append(sent.text)
    for i in sentences_list:
        doc = doc.replace(i, u"\u2588" * len(i))
    return doc,sentences_list

def output(doc,filename,path):
    outputfile = ('./files/%s.redacted' %(filename))
    with open(outputfile, "w+", encoding='utf-8') as f:
        f.write(doc)
        f.close()

def stats(doc_stats,a,filename,w):
    nlp_doc=nlp(doc_stats)
    stats_list=[]
    stats=''
    (doc_stats,names_redacted)=names(doc_stats)
    stats="The number of names redacted from the file is: %d" %len(names_redacted) + '\n'
    stats_list.append(stats)
    (doc_stats,dates_redacted)=dates(doc_stats)
    stats="The number of dates redacted from the file is: %d" %len(dates_redacted) + '\n'
    stats_list.append(stats)
    (doc_stats,phone_redacted)=phone_numbers(doc_stats)
    stats="The number of phone numbers redacted from the file is: %d" %len(phone_redacted) +'\n'
    stats_list.append(stats)
    (doc_stats,gender_redacted)=gender(doc_stats)
    stats="The number of gender terms redacted from the file is: %d" %len(gender_redacted) +'\n'
    stats_list.append(stats)
    (doc_stats,address_redacted)=address(doc_stats)
    stats="The number of addresses redacted from the file is: %d" %len(address_redacted) +'\n'
    stats_list.append(stats)
    (doc_stats,sentences_redacted)=concept(doc_stats,w)
    stats="The number of sentences redacted from the file is: %d" %len(sentences_redacted) +'\n'
    stats_list.append(stats)

    if a=='stdout':
        for i in stats_list:
            print(i)
    else:
        txtfile = ('./stderr/stderr%s' %filename)
        with open(txtfile, "w+", encoding='utf-8') as f:
            for i in stats_list:
                f.write(i)
            f.close()





