import re
from glob import glob
import operator
import os
from os.path import exists
from bs4 import BeautifulSoup
import traceback

CURRENT_DIRECTORY = os.getcwd()
INPUT_FOLDER = path = os.path.join(CURRENT_DIRECTORY,'cacm')
OUTPUT_FOLDER = path = os.path.join(CURRENT_DIRECTORY,'corpus')

def l_strip(word):
    while(word[:1] == "-" or word[:1] == "." or word[:1] == ","):
        num_format = re.compile("^[\-]?[0-9]*\.?[0-9]+$")
        isnumber = re.match(num_format,word)
        if isnumber:
            break
        elif word[:1] == "-" or word[:1] == "." or word[:1] == ",":
            word = word[1:]
        else:
            break
    return word

def strippunc(word):
    if ( (word[((len(word)) - 1):(len(word))] == ".") or (word[((len(word)) - 1):(len(word))] == ",") or (word[((len(word)) - 1):(len(word))] == "-")):
        word = word[:(len(word)-1)]
    else:
        word
    return l_strip(word)


def process_files():
    terms_from_file = {}
    urls={}
    try:
        ctr=1
        for file in glob(os.path.join(INPUT_FOLDER,'*.html')):
            url = file[(file.rindex('\\'))+1:]
            url = url.rstrip('.html')
            urls.update({file:url})
            print "Processing %s" %(file[(file.rindex('\\'))+1:])
            terms_from_file[file] = open(file, 'r').read().lower()
            content = terms_from_file[file]
            soup = BeautifulSoup(content, "html.parser")
            soup.prettify().encode("utf-8")

            total_text = soup.find('pre').get_text().encode("utf-8")
            terms_from_file[file] = total_text
            pattern = re.compile('[_!~()}{\][^?&*@\s#$%=+:;\\/|<>"\']')
            terms_from_file[file] = pattern.sub(' ',terms_from_file[file])
            terms_from_file[file] = terms_from_file[file].split()
            temp_list = []
            for terms in terms_from_file[file]:
                temp_list.append(strippunc(terms))

            while '' in temp_list:
                del temp_list[temp_list.index('')]
            terms_from_file[file] = temp_list
            ctr+=1

    except Exception as e:
        print(traceback.format_exc())
    return terms_from_file,urls



def write_files():
    try:
        LINK_FILENAME=[]
        ctr=1
        terms_from_file,urls = process_files()
        for term_file in terms_from_file.keys():
            file_name = urls[term_file]
            if file_name not in LINK_FILENAME:
                LINK_FILENAME.append(file_name)
            else:
                while(file_name in LINK_FILENAME):
                    file_name = file_name+str(ctr)
                    ctr = ctr + 1
                LINK_FILENAME.append(file_name)
            out_file  = open(OUTPUT_FOLDER+"\\"+file_name+".txt",'w')
            tokens=" ".join(terms_from_file[term_file])
            out_file.write(tokens)
            out_file.close()
    except Exception as e:
        print(traceback.format_exc())

def processed_query(unprocessed_query):
    try:
        temp_list = []
        query = unprocessed_query[unprocessed_query.find('</DOCNO>')+8:unprocessed_query.find('</DOC>')]        
        pattern = re.compile('[_%=+~()!@\s#$}{\][^?&*:;\\/|<>"\']')
        query = pattern.sub(' ',query)
        for terms in query.split():
            temp_list.append(strippunc(terms))
        while '' in temp_list:
            del temp_list[temp_list.index('')]
        query = " ".join(temp_list)
        unprocessed_query = unprocessed_query[unprocessed_query.find('</DOC>')+6:]
        return unprocessed_query,query
    except Exception as e:
        print(traceback.format_exc())


def processing_query():
    try:
        if exists(CURRENT_DIRECTORY+"\\query.txt"):
            os.remove(CURRENT_DIRECTORY+"\\query.txt")
        unprocessed_query = open(CURRENT_DIRECTORY+"\\cacm.query.txt",'r').read()
        query_file = open(CURRENT_DIRECTORY+"\\query.txt",'a')
        while unprocessed_query.find('<DOC>')!=-1:
            unprocessed_query, query = processed_query(unprocessed_query)
            if(unprocessed_query.find('<DOC>')==-1):
                query_file.write(query.lower())
            else:
                query_file.write(query.lower()+"\n")
    except Exception as e:
        print(traceback.format_exc())


def start():
	processing_query()
	write_files()
	print "\nParsing Done! Have a nice day!"

start()

