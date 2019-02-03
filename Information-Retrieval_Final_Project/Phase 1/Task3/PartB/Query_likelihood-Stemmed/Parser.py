import os
from os.path import exists
CURRENT_DIR = os.getcwd()
INPUT_FOLDER = path = os.path.join(CURRENT_DIR,'corpus')
document = open("cacm_stem.txt").read()

start_item = document.find('#')
while start_item != -1:
    doc_id = document[start_item + 2: document.find("\n",start_item + 2)]
    print doc_id
    end_item = document.find('#',document.find("\n",start_item + 2))
    contents = document[start_item + 2 : end_item]
    if len(doc_id) == 1:
        out = "CACM-000" + doc_id
    if len(doc_id) == 2:
        out = "CACM-00" + doc_id
    if len(doc_id) == 3:
        out = "CACM-0" + doc_id
    if len(doc_id) == 4:
        out = "CACM-" + doc_id
    print out 
    output_file = open(INPUT_FOLDER+"\\"+out+".txt",'w')
    output_file.write(contents)
    start_item = document.find('#',end_item)
print "Corpus Generated!"
