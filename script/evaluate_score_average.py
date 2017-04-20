import numpy as np
import sys
matrix_list = ["all", "1_syllable", "2_syllable", "3_syllable", "4_syllable", "2-_syllable"]

def relevant(query, text_id, relevant_dict):
    if text_id in relevant_dict[query]:
        return True
    return False

#def build_relevant_dict(ctm_file):
#    relevant_dict = {}
#    for line in open(ctm_file).readlines():
#        fields = line.strip().split()
#        keyword_id = fields[4]
#        text_id = fields[0]
#        if not relevant_dict.has_key(keyword_id):
#            relevant_dict[keyword_id]=[]
#        relevant_dict[keyword_id].append(text_id)
#    return relevant_dict

def build_relevant_dict(text_file):
    relevant_dict = {}
    for line in open(text_file).readlines():
        fields = line.strip().split()
        text_id = fields[0]
        for i in range(1, len(fields)):
            keyword_id = fields[i]
            if not relevant_dict.has_key(keyword_id):
                relevant_dict[keyword_id]=set()
            relevant_dict[keyword_id].add(text_id)
    return relevant_dict

def build_syllable_num_dict(syllable_num_file):
    syllable_num_dict = {}
    for line in open(syllable_num_file).readlines():
        fields = line.strip().split()
        keyword = fields[0]
        syllable_num = int(fields[1])
        syllable_num_dict[keyword]=syllable_num
    return syllable_num_dict

def average_cost(costlist, querylist):
    querylist_uniq = []
    cost_dict = {}
    for i in range(len(querylist)):
        query_id = querylist[i].strip()
        keyword = query_id.split("_")[0]
        if not cost_dict.has_key(keyword):
            querylist_uniq.append(keyword)
            cost_dict[keyword] = []
        cost_dict[keyword].append(costlist[i])
    cost_uniq = []
    for keyword in querylist_uniq:
        cost_uniq.append(np.array(cost_dict[keyword]).sum(axis=0).tolist())
    return (cost_uniq, querylist_uniq)

def evaluate(costlist, querylist, doclist, relevant_dict, syllable_num_dict):
    evaluate_matrix = {}
    for x in matrix_list:
        evaluate_matrix[x] = []
    (cost_uniq, querylist_uniq) = average_cost(costlist, querylist)

    for i in range(len(querylist_uniq)):
        ranklist = np.array(cost_uniq[i]).argsort()
        Precision = []
        num_rele = 0.0
        sum_precision = 0.0

        for j in range(len(ranklist)):
            keyword_id = querylist_uniq[i].strip().split("_")[0]
            doc_id = "_".join(doclist[ranklist[j]].strip().split("_")[:-1])
            isRele = False
            if relevant(keyword_id, doc_id, relevant_dict):
                num_rele += 1
                isRele = True
            Precision.append(num_rele/(j+1))
            if isRele == True:
                sum_precision += Precision[-1]
        N = int(num_rele)
        if (syllable_num_dict[keyword_id] == 1):
            evaluate_matrix["1_syllable"].append([sum_precision/N, Precision[N-1], Precision[9]])
        elif (syllable_num_dict[keyword_id] == 2):
            evaluate_matrix["2_syllable"].append([sum_precision/N, Precision[N-1], Precision[9]])
        elif (syllable_num_dict[keyword_id] == 3):
            evaluate_matrix["3_syllable"].append([sum_precision/N, Precision[N-1], Precision[9]])
        elif (syllable_num_dict[keyword_id] >= 4):
            evaluate_matrix["4_syllable"].append([sum_precision/N, Precision[N-1], Precision[9]])
        else:
            print("keyword: %s not find in the syllable num dictionary or syllable num wrong: %d \n"%(keyword_id, syllable_num_dict[keyword_id])) 
        if (syllable_num_dict[keyword_id] >= 2):
            evaluate_matrix["2-_syllable"].append([sum_precision/N, Precision[N-1], Precision[9]])

        evaluate_matrix["all"].append([sum_precision/N, Precision[N-1], Precision[9]])
    return evaluate_matrix

if __name__=="__main__":
    if len(sys.argv) < 6:
        print("USAGE: python %s result_dir keywordlist testlist textfile syllable_num_file"%sys.argv[0])
        exit(1)
    
    result_dir =  sys.argv[1]
    keywordlist = open(sys.argv[2]).readlines()
    testlist = open(sys.argv[3]).readlines()
    relevant_dict = build_relevant_dict(sys.argv[4])
    syllable_num_dict = build_syllable_num_dict(sys.argv[5])

    costlist = []
    for keyword in keywordlist:
        result_fid = open(result_dir + keyword.strip() + ".RESULT")
        resultlist = result_fid.readlines()
        result_fid.close()
        
        scorelist = []
        for res in resultlist:
            score = float(res.strip().split()[0])
            scorelist.append(score)
        costlist.append(scorelist)
    evaluate_matrix = evaluate(costlist, keywordlist, testlist, relevant_dict, syllable_num_dict)
    for x in matrix_list:
        output = np.array(evaluate_matrix[x]).mean(axis=0)
        MAP = output[0]
        PatN = output[1]
        Pat10 = output[2]
        print('%s: MAP=%.3f PatN=%.3f Pat10=%.3f'%(x, MAP, PatN, Pat10))

