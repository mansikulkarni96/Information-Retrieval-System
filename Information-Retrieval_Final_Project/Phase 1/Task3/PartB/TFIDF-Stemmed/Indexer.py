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

def generate_index():
    inverted_index = {}
    tokens_per_doc = {}
    try:
        counter=1
        for file in glob(os.path.join(INPUT_FOLDER,'*.txt')):
            print "Processing %s " %(file[(file.rindex('\\'))+1:])
            DOC_NAME.update({counter:file.split('corpus\\')[1][:-4]})
            doc_id = counter
            doc= open(file, 'r').read()
            tokens_per_doc.update({doc_id:len(doc.split())})
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
        for term in inverted_index:
            idf = 1.0 + log(float(total_num_of_docs) / float(len(inverted_index[term].keys()) + 1))
            for doc in inverted_index[term]:
                normalized_tf = float(inverted_index[term][doc])/float(tokens_per_doc[doc])
                inverted_index[term][doc] = normalized_tf * idf 
    except Exception as e:
        print(traceback.format_exc())
    return inverted_index,total_num_of_docs

def generate_doc_tfidf_score(query,inverted_index,total_num_of_docs):
    try:
        query_term_freq = {}
        query_term_list = query.split()
        reduced_inverted_index = {} 
        doc_score = {} 
        for term in query_term_list:
            if inverted_index.has_key(term):
                reduced_inverted_index.update({term:inverted_index[term]})
            else:
                reduced_inverted_index.update({term:{}})
        for term in reduced_inverted_index:
            for doc_id in reduced_inverted_index[term]:
                if not doc_score.has_key(doc_id):
                    doc_id_mag = fetch_doc_mag(doc_id,reduced_inverted_index)
                    doc_score.update({doc_id:doc_id_mag})
        sorted_doc_score = sorted(doc_score.items(), key=operator.itemgetter(1), reverse=True)
        write_to_file(sorted_doc_score)
    except Exception as e:
        print(traceback.format_exc())

def fetch_doc_mag(doc_id,inverted_index):
    doc_magnitude = 0
    for term in inverted_index:
        if inverted_index[term].has_key(doc_id):
            doc_magnitude += inverted_index[term][doc_id]
    return doc_magnitude


def write_to_file(sorted_doc_score):
    try:
        if(len(sorted_doc_score)>0):
            out_file  = open(OUTPUT_FOLDER_PATH+"\\Stemmed_TFIDF_doc_score.txt",'a')
            for i in range(min(100,len(sorted_doc_score))):
                doc_id,doc_score = sorted_doc_score[i]
                out_file.write(str(QUERY_ID) + " Q0 "+ DOC_NAME[doc_id] +" " + str(i+1) + " " + str(doc_score) +" TFIDF_Model_Stemmed\n")
            out_file.close()
            print "\nProcessing Query # " +str(QUERY_ID)
        else:
            print "\nTerm not found in the corpus"
    except Exception as e:
        print(traceback.format_exc())


def start():
    global QUERY_ID
    inverted_index,total_num_of_docs = generate_index()
    if exists(OUTPUT_FOLDER_PATH+"\\Stemmed_TFIDF_doc_score.txt"):
        os.remove(OUTPUT_FOLDER_PATH+"\\Stemmed_TFIDF_doc_score.txt")
    query_file = open("cacm_stem.query.txt", 'r')
    for query in query_file.readlines():
        QUERY_ID+=1
        generate_doc_tfidf_score(query,inverted_index,total_num_of_docs)
    print "\nTFIDF Score Generated! Have a nice day!"

start()
