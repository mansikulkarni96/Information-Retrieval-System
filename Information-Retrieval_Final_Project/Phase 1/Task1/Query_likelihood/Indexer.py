from glob import glob
import operator
import os
from os.path import exists
import traceback
from math import sqrt
from math import log


CURRENT_DIRECTORY = os.getcwd()
INPUT_FOLDER = path = os.path.join(CURRENT_DIRECTORY,'corpus')
OUTPUT_FOLDER_PATH = path = os.path.join(CURRENT_DIRECTORY,'output_score')
DOC_NAME ={}
QUERY_ID = 0
lambda_value = 0.35

def generate_index():
    inverted_index = {}
    words_per_doc = {}
    try:
        counter=1
        for file in glob(os.path.join(INPUT_FOLDER,'*.txt')):
            print "Processing %s " %(file[(file.rindex('\\'))+1:])
            DOC_NAME.update({counter:file.split('corpus\\')[1][:-4]})
            doc_id = counter
            doc= open(file, 'r').read()
            words_per_doc.update({doc_id:len(doc.split())-1})
            for term in doc.split():
                
                if not inverted_index.has_key(term):
                    doc_term_freq ={doc_id:1}
                    inverted_index.update({term:doc_term_freq})
                elif not inverted_index[term].has_key(doc_id):
                    inverted_index[term].update({doc_id:1})
                else:
                    inverted_index[term][doc_id] += 1
            counter+=1
        total_num_of_docs = counter-1
    except Exception as e:
        print(traceback.format_exc())
    return inverted_index,total_num_of_docs,words_per_doc



def generate_doc_query_likelihood_score(query,inverted_index,total_num_of_docs,words_per_doc):
    query_term_freq = {}
    query_term_list = query.split()
    reduced_inverted_index = {}
    try:
        for term in query_term_list:
            if not query_term_freq.has_key(term):
                query_term_freq.update({term:1})
            else:
                query_term_freq[term]+=1
        for term in query_term_freq:
            query_term_freq[term] = float(query_term_freq[term])/float(len(query_term_list))
            if inverted_index.has_key(term):
                reduced_inverted_index.update({term:inverted_index[term]})
            else:
                reduced_inverted_index.update({term:{}})

        query_likelihood(query_term_freq,reduced_inverted_index,total_num_of_docs,words_per_doc)

    except Exception as e:
        print(traceback.format_exc())

def query_likelihood(query_term_freq,reduced_inverted_index,total_num_of_docs,words_per_doc):
    doc_score={}
    doc_score=dict.fromkeys(doc_score, 0)
    per_query={}
    dict_query_doc={}
    total_words=0


    for i in words_per_doc:
        total_words+=words_per_doc[i]

    for term in query_term_freq:
        corpus_query_sum=0
        value2=0
        for item in reduced_inverted_index[term]:
             corpus_query_sum+=reduced_inverted_index[term][item]
        value2= lambda_value*(float(float(corpus_query_sum)/float(total_words)))
        per_query[term]=value2


    for term in query_term_freq:
        sum=0
        freq_query_doc=0
        value=0
        for item in reduced_inverted_index[term]:

            value= float(float(reduced_inverted_index[term][item])/float(words_per_doc[item]))

            final_value=(1-lambda_value)*value+per_query[term]

            final_value2= log(final_value,10)
           
            if item in doc_score:
                doc_score[item]+=final_value2
            else:
                doc_score[item]=final_value2
    sorted_doc_scores = sorted(doc_score.items(), key=lambda e: e[1], reverse=False)
    write_doc_score(sorted_doc_scores)

def write_doc_score(sorted_doc_score):
    try:
        if(len(sorted_doc_score)>0):
            out_file  = open(OUTPUT_FOLDER_PATH+"\\SQL_doc_score.txt",'a')
            for i in range(min(100,len(sorted_doc_score))):
                doc_id,doc_score = sorted_doc_score[i]
                out_file.write(str(QUERY_ID) + " Q0 "+ DOC_NAME[doc_id] +" " + str(i+1) + " " + str(doc_score) +" Smoothed_Query_Likelihood_Model\n")            
            out_file.close()
            print "\nProcessing Query # " +str(QUERY_ID) 
        else:
            print "\nQuery Term not found in the corpus"
    except Exception as e:
        print(traceback.format_exc())


def start():
    global QUERY_ID
    inverted_index,total_num_of_docs,words_per_doc = generate_index()
    if exists(OUTPUT_FOLDER_PATH+"\\SQL_doc_score.txt"):
        os.remove(OUTPUT_FOLDER_PATH+"\\SQL_doc_score.txt")
    query_file = open("query.txt", 'r')
    for query in query_file.readlines():
        QUERY_ID+=1
        generate_doc_query_likelihood_score(query,inverted_index,total_num_of_docs,words_per_doc)
    print "\nSmoothed Query Likelihood score generated! Have a nice day!"

start()