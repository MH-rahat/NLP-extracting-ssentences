# -*- coding: utf-8 -*-
"""
@author: mahamudulrahat94
"""

#import necessary libraries
import spacy   
from spacy.matcher import Matcher
from spacy.util import filter_spans
import pandas as pd
nlp = spacy.load('en_core_web_sm') 

#import the data
data=pd.read_csv('Company descriptions-Grid view.csv')
data.dropna(axis='index',inplace=True)#to remove any blank details
data=data.reset_index()#updating the index

#important part of the code
stop_words=['founded','supports','supported','visualizes',
            'believe','believes','partnered','partner','retrieves','brand','based']

company_number=50#selecting how many comapnies to extract data
companies=[ ]
summary_list=[ ]
for qq in range(0,company_number):
    text=data['Description'][qq]
    sentence = text
    #these are the rules to specify the grammer
    #   ? Make the pattern optional, by allowing it to match 0 or 1 times.
    #   + Require the pattern to match 1 or more times
    #   * Allow the pattern to match zero or more times.
    pattern = [{'POS': 'VERB','OP': '+'}, #OP means how you want the rule to be,such as have to match more than 1 times or can be zero times or can be zero or one times   
               {'OP': '*'},
               {'POS': 'NOUN', 'OP': '+'},
               {'POS':'PUNCT'}
               ]
               
    
    # instantiate a Matcher instance
    matcher = Matcher(nlp.vocab)
    matcher.add("Verb phrase", None, pattern)
    
    doc = nlp(sentence)
    
    #finding the company name
    token_dict={}
    for tok in doc: 
            token_dict[tok.idx]=str(tok.text)
    company_name=token_dict[0]
    companies.append(company_name)#storing in a list to use later
    
    # call the matcher to find matches 
    matches = matcher(doc)
    spans = [doc[start:end] for _, start, end in matches]
    summary_text=[ ]
    for match_id, start, end in matches:
        # Get the string representation 
        string_id = nlp.vocab.strings[match_id]  
        span = doc[start:end]  # The matched span
        summary_text.append(span.text)
    #print('++++'+text)
    summary=summary_text[-1]#reversed the list to find the largest string
    #print('****'+'\n'+summary)
    
    #filtering the summary further
    
    doc_summary = nlp(summary)
    doc_sentences = list(doc_summary.sents)
    
    #storing the sentences in a list
    doc_sentences_c=[ ]
    for sentence in doc_sentences:
           doc_sentences_c.append(str(sentence)) 
           
    to_del=[ ]
    to_keep=[ ]#to find the indexes of the sentence to keep
    for i in range(0,len(doc_sentences_c)):#working with each sentence
        s_nlp=nlp(str(doc_sentences_c[i]).lower())
        
        p=0
        for tok in s_nlp: 
               if tok.text in stop_words:#checking if the sentence contain stop word
                   to_del.append(i)#you can delete this line if you want
                   p=1
            #making sure  the sentence does not contain any stop words
               elif p==0:
                   to_keep.append(i)#taking the indexes
    
                   
    to_keep=list(set(to_keep))#converting to 'set' to find the unique value and again converted to list
    final_summary=''
    for x in range(0,len(to_keep)):
        id=to_keep[x]
        final_summary+=doc_sentences_c[id]
    summary_list.append(final_summary)#appended all the summary together 
    # final_summary=final_summary.replace('They',company_name,1)
    # final_summary='The company name is '+company_name+'.'+final_summary

#created a new dataframe to store the new values
new_df=pd.DataFrame()  
new_df['Company']=companies
new_df['Description']=data['Description'].loc[0:company_number]
new_df['Summary']=summary_list

new_df.to_csv('extracted50.csv')
    

