import numpy as np
import sys
import evaluate as EV

matrix_list = ["all", "1_syllable", "2_syllable", "3_syllable", "4_syllable", "2-_syllable"]

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


if __name__=="__main__":
    if len(sys.argv) < 6:
        print("USAGE: python %s result_dir keywordlist testlist textfile syllable_num_file"%sys.argv[0])
        exit(1)
    
    result_dir =  sys.argv[1]
    keyword_list = open(sys.argv[2]).readlines()
    test_list = open(sys.argv[3]).readlines()
    occurance_dict = EV.build_occurance_dict(sys.argv[4])
    syllable_num_dict = EV.build_syllable_num_dict(sys.argv[5])

    cost_list = []
    for keyword in keyword_list:
        result_fid = open(result_dir + keyword.strip() + ".RESULT")
        result_list = result_fid.readlines()
        result_fid.close()
        
        score_list = []
        for res in result_list:
            score = float(res.strip().split()[0])
            score_list.append(score)
        cost_list.append(score_list)

    (cost_uniq, keyword_list_uniq) = average_cost(cost_list, keyword_list)
    evaluate_matrix = EV.evaluate(cost_uniq, keyword_list_uniq, test_list, occurance_dict, syllable_num_dict)
    for x in matrix_list:
        output = np.array(evaluate_matrix[x]).mean(axis=0)
        MAP = output[0]
        PatN = output[1]
        Pat10 = output[2]
        print('%s: MAP=%.3f PatN=%.3f Pat10=%.3f'%(x, MAP, PatN, Pat10))

