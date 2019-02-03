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
DOC_LENGTH = {}
QUERY_ID = 0
AVDL = 0
k1 = 1.2
k2 = 100
b = 0.75

def generate_index():
    global DOC_LENGTH
    inverted_index = {}
    try:
        ctr=1
        for file in glob(os.path.join(INPUT_FOLDER,'*.txt')):
            print "Processing %s " %(file[(file.rindex('\\'))+1:])
            DOC_NAME.update({ctr:file.split('corpus\\')[1][:-4]})
            doc_id = ctr
            doc= open(file, 'r').read()
            DOC_LENGTH.update({doc_id:len(doc.split())})
            with open('common_words') as f:
                stopwords = f.read().splitlines()

            for term in doc.split():
                if term not in stopwords:
                    if not inverted_index.has_key(term):
                        doc_term_freq ={doc_id:1}
                        inverted_index.update({term:doc_term_freq})
                    elif not inverted_index[term].has_key(doc_id):
                        inverted_index[term].update({doc_id:1})
                        
                    else:
                        inverted_index[term][doc_id] += 1
            ctr+=1
        total_num_of_docs = ctr-1
    except Exception as e:
        print(traceback.format_exc())
    return inverted_index,total_num_of_docs

def generate_doc_bm25_score(query,inverted_index,total_num_of_docs,relevant_list):
    try:
        query_term_freq = {}
        query_term_list = query.split()
        reduced_inverted_index = {}
        with open('common_words') as f:
            stopwords = f.read().splitlines()

        for term in query_term_list:
            if term not in stopwords:
                if not query_term_freq.has_key(term):
                    query_term_freq.update({term:1})
                else:
                    query_term_freq[term]+=1

        for term in query_term_freq:
            if inverted_index.has_key(term):
                reduced_inverted_index.update({term:inverted_index[term]})
            else:
                reduced_inverted_index.update({term:{}})
        process_score(query_term_freq,reduced_inverted_index,total_num_of_docs,relevant_list)
    except Exception as e:
        print(traceback.format_exc())

def get_relevant_numb(doc_list,relevant_list):
    try:
        ctr = 0
        for doc_id in doc_list:
            if doc_id in relevant_list:
                ctr+=1
        return ctr
    except Exception as e:
        print(traceback.format_exc())

def calculate_BM25(n, f, qf, r, N, dl,R):
    try:
       
        K = k1 * ((1 - b) + b * (float(dl) / float(AVDL)))
        number1 = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
        number2 = ((k1 + 1) * f) / (K + f)
        number3 = ((k2 + 1) * qf) / (k2 + qf)
        return number1 * number2 * number3
    except Exception as e:
        print(traceback.format_exc())

def process_score(query_term,inverted_index,N,relevant_list):
    doc_score={}
    R = len(relevant_list)
    try:
        for term in inverted_index:
            n = len(inverted_index[term])
            dl = 0
            qf = query_term[term]
            r = get_relevant_numb(inverted_index[term],relevant_list)
            for doc_id in inverted_index[term]:
                f = inverted_index[term][doc_id]
                if DOC_LENGTH.has_key(doc_id):
                    dl = DOC_LENGTH[doc_id]
                score = calculate_BM25(n, f, qf, r, N, dl,R)
                if doc_id in doc_score:
                    total_score = doc_score[doc_id] + score
                    doc_score.update({doc_id:total_score})
                else:
                    doc_score.update({doc_id:score})
        sorted_doc_score = sorted(doc_score.items(), key=operator.itemgetter(1), reverse=True)
        write_to_file(sorted_doc_score)
    except Exception as e:
        print(traceback.format_exc())

def write_to_file(sorted_doc_score):
    try:
        if(len(sorted_doc_score)>0):
            out_file  = open(OUTPUT_FOLDER_PATH+"\\BM25_stopped_doc_score.txt",'a')
            for i in range(min(100,len(sorted_doc_score))):
                doc_id,doc_score = sorted_doc_score[i]
                out_file.write(str(QUERY_ID) + " Q0 "+ DOC_NAME[doc_id] +" " + str(i+1) + " " + str(doc_score) +" BM25_Model_Stopped\n")
            out_file.close()
            print "\nProcessing Query # " +str(QUERY_ID)
        else:
            print "\nTerm not found in the corpus"
    except Exception as e:
        print(traceback.format_exc())

def get_relevant_list():
    try:
        file_list = []
        rel_doc_id = []
        rel_file = open('cacm.rel.txt','r')
        for line in rel_file.readlines():
            params = line.split()
            if params and (params[0] == str(QUERY_ID)):
                file_list.append(params[2])
        for doc_id in DOC_NAME:
            if DOC_NAME[doc_id] in file_list:
                rel_doc_id.append(doc_id)
        rel_file.close()
        return rel_doc_id
    except Exception as e:
        print(traceback.format_exc())

def generate_avdl():
    try:
        sum = 0
        for doc_id in DOC_LENGTH:
            sum+=DOC_LENGTH[doc_id]
        return (float(sum)/float(len(DOC_LENGTH)))
    except Exception as e:
        print(traceback.format_exc())

def start():
    try:
        global QUERY_ID,AVDL
        inverted_index,total_num_of_docs = generate_index()
        AVDL = generate_avdl()
        if exists(OUTPUT_FOLDER_PATH+"\\BM25_stopped_doc_score.txt"):
            os.remove(OUTPUT_FOLDER_PATH+"\\BM25_stopped_doc_score.txt")
        query_file = open("query.txt", 'r')
        for query in query_file.readlines():
            QUERY_ID+=1
            relevant_list = get_relevant_list()
            generate_doc_bm25_score(query,inverted_index,total_num_of_docs,relevant_list)
        print "\nBM25 Score Generated. Have a great day!"
    except Exception as e:
        print(traceback.format_exc())
        
start()
