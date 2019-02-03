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
DOC_NAME ={} # mapping doc name and ids
DOC_LENGTH = {} # mapping the length and the doc_id
QUERY_ID = 0
AVDL = 0
flag = 1
k1 = 1.2
k2 = 100
b = 0.75

def generate_index():
    global DOC_LENGTH
    inverted_index = {}
    try:
        ctr=1
        for file in glob(os.path.join(INPUT_FOLDER,'*.txt')):
            print "Processing %s - " %(file[(file.rindex('\\'))+1:])
            DOC_NAME.update({ctr:file.split('corpus\\')[1][:-4]})
            doc_id = ctr
            doc= open(file, 'r').read()
            DOC_LENGTH.update({doc_id:len(doc.split())})
            for term in doc.split():
                if not inverted_index.has_key(term):
                    doc_term_freq ={doc_id:1}
                    inverted_index.update({term:doc_term_freq})
                elif not inverted_index[term].has_key(doc_id):
                    inverted_index[term].update({doc_id:1})
                else:
                    inverted_index[term][doc_id] += 1
            ctr=ctr+1
        total_num_of_docs = ctr-1
    except Exception as e:
        print(traceback.format_exc())
    return inverted_index,total_num_of_docs

def generate_doc_bm25_score(query,inverted_index,total_num_of_docs,relevant_list):
    query_term_freq = {}
    query_term_list = query.split()
    reduced_inverted_index = {} # filtered inverted index containing only the query terms
    for term in query_term_list:
        if not query_term_freq.has_key(term):
            query_term_freq.update({term:1})
        else:
            query_term_freq[term]+=1
    for term in query_term_freq:
        if inverted_index.has_key(term):
            reduced_inverted_index.update({term:inverted_index[term]})
        else:
            reduced_inverted_index.update({term:{}})
    process_score(query_term_freq,reduced_inverted_index,total_num_of_docs,relevant_list,query,inverted_index)

def get_relevant_numb(doc_list,relevant_list):
    ctr = 0
    for doc_id in doc_list:
        if doc_id in relevant_list:
            ctr+=1
    return ctr


def calculate_BM25(n, f, qf, r, N, dl,R):
    K = k1 * ((1 - b) + b * (float(dl) / float(AVDL)))
    number1 = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    number2 = ((k1 + 1) * f) / (K + f)
    number3 = ((k2 + 1) * qf) / (k2 + qf)
    return number1 * number2 * number3

def process_score(query_term,inverted_index,N,relevant_list,query,index):
    global flag
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
        if flag == 1:
            pseudo_relevance_feedback(sorted_doc_score,query,index,N,relevant_list)
        if flag == 2:
            flag = 1
            write_to_file(sorted_doc_score)
    except Exception as e:
        print(traceback.format_exc())

def pseudo_relevance_feedback(sorted_doc_score,query,inverted_index,total_num_of_docs,relevant_list):
    global flag
    new_query = query
    relevance_index = {}
    non_relevance_index = {}
    magnitude_relevant = 0
    magnitude_non_relevant = 0
    query_vector = {}
    updated_query = {}
    flag += 1
    k = 10
    # making the query vector
    for term in query.split():
        if query_vector.has_key(term):
            query_vector[term] +=1
        else:
            query_vector[term] = 1
    for term in inverted_index:
        if not query_vector.has_key(term):
            query_vector[term] = 0
    print "query vector generated"
    #creating the relevant document set vector
    for i in range(0,k):
        doc_id,doc_score = sorted_doc_score[i]
        doc= open(INPUT_FOLDER+"\\"+DOC_NAME[doc_id]+".txt").read()
        for term in doc.split():
            if relevance_index.has_key(term):
                relevance_index[term] += 1
            else:
                relevance_index[term] = 1

    for term in inverted_index:
        if relevance_index.has_key(term):
            relevance_index[term] = relevance_index[term]
        else:
            relevance_index[term] = 0
    # calculating the magnitude

    for term in relevance_index:
        magnitude_relevant += float(relevance_index[term]**2)
        magnitude_relevant = float(sqrt(magnitude_relevant))
    print "relevant magnitude" + str(magnitude_relevant)



    for i in range(k+1,len(sorted_doc_score)):
        doc_id,doc_score = sorted_doc_score[i]
        doc= open(INPUT_FOLDER+"\\"+DOC_NAME[doc_id]+".txt").read()
        for term in doc.split():
            if non_relevance_index.has_key(term):
                non_relevance_index[term] += 1
            else:
                non_relevance_index[term] = 1

    for term in inverted_index:
        if non_relevance_index.has_key(term):
            non_relevance_index[term] = non_relevance_index[term]
        else:
            non_relevance_index[term] = 0
    print "non relevant vector generated"

    for term in non_relevance_index:
        magnitude_non_relevant += float(non_relevance_index[term]**2)
    magnitude_non_relevant = float(sqrt(magnitude_non_relevant))

    print "non-relevant magnitude" + str(magnitude_non_relevant)
    # calculating the new query
    print "Implementing Rocchio algorithm"
    for term in inverted_index:
        updated_query[term] = query_vector[term] + (0.5/magnitude_relevant) * relevance_index[term] - (0.15/magnitude_non_relevant) * non_relevance_index[term]

    # storing the sorted array
    sorted_updated_query = sorted(updated_query.items(), key=operator.itemgetter(1), reverse=True)
    

    for i in range(20):
        term,frequency = sorted_updated_query[i]
        if term not in query:
            new_query +=  " "
            new_query +=  term
    # new BM25 values generated
    generate_doc_bm25_score(new_query,inverted_index,total_num_of_docs,relevant_list)

def write_to_file(sorted_doc_score):

    if(len(sorted_doc_score)>0):
        out_file  = open(OUTPUT_FOLDER_PATH+"\\BM25_rel_feed_doc_score.txt",'a')
        for i in range(min(100,len(sorted_doc_score))):
            doc_id,doc_score = sorted_doc_score[i]
            out_file.write(str(QUERY_ID) + " Q0 "+ DOC_NAME[doc_id] +" " + str(i+1) + " " + str(doc_score) +" BM25_Model\n")
        out_file.close()
        print "\nProcessing Query # " +str(QUERY_ID)
    else:
        print "\nTerm not found"

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

def get_avdl():
    sum = 0
    for doc_id in DOC_LENGTH:
        sum+=DOC_LENGTH[doc_id]
    avdl_val = float(sum)/float(len(DOC_LENGTH))
    return avdl_val

def start():
    global QUERY_ID,AVDL,flag
    inverted_index,total_num_of_docs = generate_index()
    AVDL = get_avdl()
    if exists(OUTPUT_FOLDER_PATH+"\\BM25_rel_feed_doc_score.txt"):
        os.remove(OUTPUT_FOLDER_PATH+"\\BM25_rel_feed_doc_score.txt")
    query_file = open("query.txt", 'r')
    for query in query_file.readlines():
        flag = 1
        QUERY_ID+=1
        relevant_list = get_relevant_list()
        generate_doc_bm25_score(query,inverted_index,total_num_of_docs,relevant_list)
    print "\nBM25 Pseudo Relevance Feedback score generated. Have a nice day!"

start()
