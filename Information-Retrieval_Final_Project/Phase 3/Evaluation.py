from os.path import exists
import traceback


N = 0 #Number of Queries
FILE_NAME = ""
RELEVANT_DICT = {}
RANK_DICT = {}


def get_file_values():
    global N,FILE_NAME
    FILE_NAME = raw_input(">\nEnter the file name of the doc_score with extension\n")
    if exists(FILE_NAME):
        file_relevant = open('cacm.rel.txt', 'r')
        file_rank_list = open (FILE_NAME, 'r')

        for line in file_relevant.readlines():
            query_key = line.split()[0]
            if not RELEVANT_DICT.has_key(query_key):
                RELEVANT_DICT[query_key] = [line[:-1]]
            else:
                content = RELEVANT_DICT.get(query_key)
                content.append(line[:-1])

        file_relevant.flush()
        file_relevant.close()

        for line in file_rank_list.readlines():
            query_key = line.split()[0]
            if not RANK_DICT.has_key(query_key):
                RANK_DICT[query_key] = [line[:-1]]
            else:
                content = RANK_DICT.get(query_key)
                content.append(line[:-1])

        N = len(RANK_DICT)
        file_rank_list.flush()
        file_rank_list.close()
    else:
        print "The file does not exist"


def evaluate_MRR():

    query_ID = 1
    reciprocal_ranking = 0

    while query_ID != N+1:

        if not RELEVANT_DICT.get(str(query_ID)):
            reciprocal_ranking += 0
            query_ID += 1
            continue

        relevant_doc_list = RELEVANT_DICT[str(query_ID)]
        ranked_doc_list = RANK_DICT[str(query_ID)]

        for doc in ranked_doc_list:
            flag_break = False
            docID = doc.split()[2]
            for rel_doc in relevant_doc_list:
                if docID == rel_doc.split()[2]:
                    reciprocal_ranking += 1.0 / float(doc.split()[3])
                    flag_break = True
                    break
            if flag_break == True:
                break
        query_ID += 1

    mean_reciprocal_ranking = reciprocal_ranking / float(N)
    return str(mean_reciprocal_ranking)

def evaluate_pk_measure():
    try:

        
        filename = FILE_NAME[:FILE_NAME.rindex('.')]
        outfilepk5 = open(filename+"_p_at_5_score.txt",'w')
        outfilepk20 = open(filename+"_p_at_20_score.txt",'w')

        p_at_k_5_dict = {}
        p_at_k_20_dict = {}
        query_ID = 1

        while query_ID != N+1:

            if not RELEVANT_DICT.get(str(query_ID)):
                p_at_k_5_dict[query_ID] = 0.0
                p_at_k_20_dict[query_ID] = 0.0
                query_ID += 1
                continue

            relevant_doc_list = RELEVANT_DICT[str(query_ID)]
            top_5_ranked_doc_list = RANK_DICT[str(query_ID)][:5]
            top_20_ranked_doc_list = RANK_DICT[str(query_ID)][:20]

            rel_number_of_docs_top5 = 0
            for doc in top_5_ranked_doc_list:
                docID = doc.split()[2]
                for rel_doc in relevant_doc_list:
                    if docID == rel_doc.split()[2]:
                        rel_number_of_docs_top5 += 1

            p_at_k_5_dict[query_ID] = rel_number_of_docs_top5 / 5.0
            outfilepk5.write(str(query_ID) + " "+ str(p_at_k_5_dict[query_ID]) +" pk_5_Model\n")


            rel_number_of_docs_top20 = 0
            for doc in top_20_ranked_doc_list:
                docID = doc.split()[2]
                for rel_doc in relevant_doc_list:
                    if docID == rel_doc.split()[2]:
                        rel_number_of_docs_top20 += 1

            p_at_k_20_dict[query_ID] = rel_number_of_docs_top20 / 20.0
            outfilepk20.write(str(query_ID) + " "+ str(p_at_k_20_dict[query_ID]) +" pk_20_Model\n")
            query_ID += 1
        outfilepk20.close()
        outfilepk5.close()
    except Exception as e:
        print(traceback.format_exc())


def evaluate_precision_and_recall(MRR):
    try:

        precision_dict = {}
        recall_dict = {}
        sum_average_precision = 0
        filename = FILE_NAME[:FILE_NAME.rindex('.')]
        outfile = open(filename+"_precision_recall.txt",'w')
        for query in RANK_DICT:
            average_precision = 0
            number_of_docs = 0
            counter = 0
            precision_sum = 0

            if not RELEVANT_DICT.get(str(query)):
                precision_dict[query] = []
                recall_dict[query] = []
                outfile.write("\nPrecision and Recall of Query # "+ str(query)+" is 0, as it has no relevance set\n")
                continue


            relevant_doc_list = RELEVANT_DICT[query]
            relevant_doc_count = len(relevant_doc_list)
            precision_dict[query] = []
            recall_dict[query] = []
            for doc in RANK_DICT[query]:
                number_of_docs +=1
                docID = doc.split()[2]
                doc_rank = doc.split()[3]
                doc_score = doc.split()[4]
                bool_doc_encounter = False
                for rel_doc in relevant_doc_list:
                    if docID ==  rel_doc.split()[2]:
                        bool_doc_encounter = True
                        break;
                if bool_doc_encounter:
                    counter = counter + 1
                    
                    recall = float(counter) / float(relevant_doc_count)
                    recall_dict[query].append({docID : recall})
                    precision = float(counter) / float(number_of_docs)
                    precision_sum = precision_sum + precision
                    precision_dict[query].append({docID : precision})
                    outfile.write(str(query) +" Q0 "+docID+" "+str(doc_rank)+" "+str(doc_score)+" R "+str(precision)+" "+str(recall)+"\n")
                else:
                    
                    recall = float(counter) / float(relevant_doc_count)
                    recall_dict[query].append({docID : recall})
                    precision = float(counter) / float(number_of_docs)
                    precision_dict[query].append({docID : precision})
                    outfile.write(str(query) +" Q0 "+docID+" "+str(doc_rank)+" "+str(doc_score)+" N "+str(precision)+" "+str(recall)+"\n")
            if counter != 0:
                average_precision = average_precision + float(precision_sum) / float(counter)
            else:
                average_precision = 0
            outfile.write("\n#############################################################")
            outfile.write("\n\tAverage Precision for query # "+ str(query) +" is: " + str(average_precision))
            outfile.write("\n#############################################################\n\n")

            sum_average_precision = sum_average_precision + average_precision

        mean_average_precision = float(sum_average_precision) / float(N)
        outfile.write("\n\tMean average precision is: " + str(mean_average_precision)+"\n")
        outfile.write("\n\tMean Reciprocal Rank is: " + str(MRR)+"\n")
        outfile.close()
    except Exception as e:
        print(traceback.format_exc())


# main function
def start():

    
    get_file_values()
    print "Initiating.."
    MRR= evaluate_MRR()
    evaluate_pk_measure()
    evaluate_precision_and_recall(MRR)
    print "Evaluation Done! Have a nice day!"

start()
