from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from rest_framework.response import Response
from sentence_transformers import SentenceTransformer as st
import numpy as np

class prod(APIView):
  def get(self,request,format=None):
    return Response("hi")
  def post(self,request,format=None):
    a=request.data
    text=a['text']

    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    per=0.5
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    print(summary)
    return Response(summary)


class comp(APIView):
    def post(self,request,format=None):
        nlp=spacy.load("en_core_web_Ig")
        doc="i love you"
        doc2="l like you"
        return Response(doc.similaririty(doc2))
        
     

