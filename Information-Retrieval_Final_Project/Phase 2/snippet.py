import traceback
import operator
from os.path import exists
import os
from bs4 import BeautifulSoup
from colorama import *

CURRENT_DIRECTORY = os.getcwd()
CACM = path = os.path.join(CURRENT_DIRECTORY,'cacm')
Output_score_loc = path = os.path.join(CURRENT_DIRECTORY,'output_score')

def processed_query(unprocessed_query):
    temp_list = []
    q = unprocessed_query[unprocessed_query.find('</DOCNO>')+8:unprocessed_query.find('</DOC>')]
    q = q.strip()
    temp_list = q.split()
    q = " ".join(temp_list)
    unprocessed_query = unprocessed_query[unprocessed_query.find('</DOC>')+6:]
    return unprocessed_query,q


def processing_query():
    try:
        if exists(CURRENT_DIRECTORY+"\\unprocessed_query.txt"):
            os.remove(CURRENT_DIRECTORY+"\\unprocessed_query.txt")
        unprocessed_query = open(CURRENT_DIRECTORY+"\\cacm.query.txt",'r').read()
        query_file = open(CURRENT_DIRECTORY+"\\unprocessed_query.txt",'a')
        while unprocessed_query.find('<DOC>')!=-1:
            unprocessed_query, query = processed_query(unprocessed_query)
            if(unprocessed_query.find('<DOC>')==-1):
                query_file.write(query)
            else:
                query_file.write(query+"\n")
    except Exception as e:
        print(traceback.format_exc())

def calculate_snippet_with_trigrams(term_list,file_name):
    try:
        lookahead = 40
        posttail = 50
        content = open(CACM+"\\"+file_name+".html",'r').read()
        soup = BeautifulSoup(content, "html.parser")
        soup.prettify().encode("utf-8")
        given_file = soup.find('pre').get_text().encode("utf-8")
        for i in range(len(term_list) - 2):
            term = term_list[i]+" "+term_list[i+1]+" "+term_list[i+2]
            if(given_file.find(term)!=-1):
                start_pos = max(given_file.index(term)-lookahead, 0)
                if start_pos!=0:
                    while start_pos > 0:
                        if given_file[(start_pos-1):start_pos] not in [" ","\n"]:
                            start_pos-=1
                        else:
                            break
                sum = given_file.index(term) +  len(term) + posttail
                end_pos = min(sum, len(given_file))
                if end_pos!=len(given_file):
                    while end_pos < len(given_file):
                        if given_file[end_pos:(end_pos+1)] not in [" ","\n"]:
                            end_pos+=1
                        else:
                            break
                first = given_file[start_pos:given_file.index(term)]
                second = given_file[given_file.index(term):(given_file.index(term)+len(term))]
                third = given_file[(given_file.index(term)+len(term)):end_pos]
                return first, second, third
        return False, False, False
    except Exception as e:
        print(traceback.format_exc())

def calculate_snippet_with_bigrams(term_list,file_name):
    try:
        lookahead = 40
        posttail = 50
        content = open(CACM+"\\"+file_name+".html",'r').read()
        soup = BeautifulSoup(content, "html.parser")
        soup.prettify().encode("utf-8")
        given_file = soup.find('pre').get_text().encode("utf-8")
        for i in range(len(term_list) - 1):
            term = term_list[i]+" "+term_list[i+1]
            if(given_file.find(term)!=-1):
                start_pos = max(given_file.index(term)-lookahead, 0)
                if start_pos!=0:
                    while start_pos > 0:
                        if given_file[(start_pos-1):start_pos] not in [" ","\n"]:
                            start_pos-=1
                        else:
                            break
                sum = given_file.index(term) +  len(term) + posttail
                end_pos = min(sum, len(given_file))
                if end_pos!=len(given_file):
                    while end_pos < len(given_file):
                        if given_file[end_pos:(end_pos+1)] not in [" ","\n"]:
                            end_pos+=1
                        else:
                            break
                first = given_file[start_pos:given_file.index(term)]
                second = given_file[given_file.index(term):(given_file.index(term)+len(term))]
                third = given_file[(given_file.index(term)+len(term)):end_pos]
                return first, second, third
        return False, False, False
    except Exception as e:
        print(traceback.format_exc())

def calculate_snippet_with_unigram(term_list,file_name):
    try:
        lookahead = 40
        posttail = 50
        content = open(CACM+"\\"+file_name+".html",'r').read()
        soup = BeautifulSoup(content, "html.parser")
        soup.prettify().encode("utf-8")
        given_file = soup.find('pre').get_text().encode("utf-8")
        for term in term_list:
            if(given_file.find(term)!=-1):
                start_pos = max(given_file.index(term)-lookahead, 0)
                if start_pos!=0:
                    while start_pos > 0:
                        if given_file[(start_pos-1):start_pos] not in [" ","\n"]:
                            start_pos-=1
                        else:
                            break
                sum = given_file.index(term) +  len(term) + posttail
                end_pos = min(sum, len(given_file))
                if end_pos!=len(given_file):
                    while end_pos < len(given_file):
                        if given_file[end_pos:(end_pos+1)] not in [" ","\n"]:
                            end_pos+=1
                        else:
                            break
                first = given_file[start_pos:given_file.index(term)]
                second = given_file[given_file.index(term):(given_file.index(term)+len(term))]
                third = given_file[(given_file.index(term)+len(term)):end_pos]
                return first, second, third
        return False, False, False
    except Exception as e:
        print(traceback.format_exc())


def calculate_snippet(query,file_name):
    term_list = query.split()
    if len(term_list) > 2:
        first, second, third = calculate_snippet_with_trigrams(term_list,file_name)
        if first != False:
            print "\nFile:"+file_name
            print first+" "+"\033[47;30m"+second+"\033[m"+" "+third
        else:
            first, second, third = calculate_snippet_with_bigrams(term_list,file_name)
            if first != False:
                print "\nFile:"+file_name
                print first+" "+"\033[47;30m"+second+"\033[m"+" "+third
            else:
                first, second, third = calculate_snippet_with_unigram(term_list,file_name)
                if first != False:
                    print "\nFile:"+file_name
                    print first+" "+"\033[47;30m"+second+"\033[m"+" "+third
                else:
                    print"no query term found in " + file_name
    elif len(term_list) > 1:
        first, second, third = calculate_snippet_with_bigrams(term_list,file_name)
        if first != False:
            print "\nFile:"+file_name
            print first+" "+"\033[47;30m"+second+"\033[m"+" "+third
        else:
            first, second, third = calculate_snippet_with_unigram(term_list,file_name)
            if first != False:
                print "\nFile:"+file_name
                print first+" "+"\033[47;30m"+second+"\033[m"+" "+third
            else:
                print"no query term found in " + file_name
    else:
        first, second, third = calculate_snippet_with_unigram(term_list,file_name)
        if first != False:
            print "\nFile:"+file_name
            print first+" "+"\033[47;30m"+second+"\033[m"+" "+third
        else:
           	print"no query term found in " + file_name

def get_list_of_files(query_id):
    file_list = []
    doc_score_file = open(Output_score_loc+"\\BM25_doc_score.txt")
    for line in doc_score_file.readlines():
        params = line.split()
        if params[0] == str(query_id):
            file_list.append(params[2])
    doc_score_file.close()
    return file_list

def start():
    try:
        init()
        processing_query()
        query_id = 0
        unprocessed_Query = open('unprocessed_query.txt','r')
        for query in unprocessed_Query.readlines():
            query_id+=1
            list_of_files = get_list_of_files(query_id)
            for file_name in list_of_files:                
                calculate_snippet(query,file_name)
    except Exception as e:
        print(traceback.format_exc())
start()
