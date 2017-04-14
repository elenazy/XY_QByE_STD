import numpy as np
import sys

def relevant(query, text_id, relevant_dict):
    if text_id in relevant_dict[query]:
        return True
    return False

def build_relevant_dict(ctm_file):
    relevant_dict = {}
    for line in open(ctm_file).readlines():
        fields = line.strip().split()
        keyword_id = fields[4]
        text_id = fields[0]
        if not relevant_dict.has_key(keyword_id):
            relevant_dict[keyword_id]=[]
        relevant_dict[keyword_id].append(text_id)
    return relevant_dict

def evaluate(costlist, querylist, doclist, relevant_dict):
    PatNset = []
    APset = []
    Pat10set = []
    for i in range(len(querylist)):
        ranklist = np.array(costlist[i]).argsort()
        Precision = []
        num_rele = 0.0
        sum_precision = 0.0

        for j in range(len(ranklist)):
            keyword_id = querylist[i].strip().split("_")[0]
            doc_id = "_".join(doclist[ranklist[j]].strip().split("_")[:-1])
            isRele = False
            if relevant(keyword_id, doc_id, relevant_dict):
                num_rele += 1
                isRele = True
            Precision.append(num_rele/(j+1))
            if isRele == True:
                sum_precision += Precision[-1]
        Pat10set.append(Precision[9])
        N = int(num_rele)
        PatNset.append(Precision[N-1])
        APset.append(sum_precision/N)
        #print(str(APset[-1]) + "\t" + str(PatNset[-1]) + "\t" + str(Pat10set[-1]))
    num_of_querys = len(querylist)
    MAP = sum(APset)/num_of_querys
    PatN = sum(PatNset)/num_of_querys
    Pat10 = sum(Pat10set)/num_of_querys
    return MAP,PatN,Pat10

if __name__=="__main__":
    if len(sys.argv) < 5:
        print("USAGE: python %s result_dir keywordlist testlist ctmfile"%sys.argv[0])
        exit(1)
    
    result_dir =  sys.argv[1]
    keywordlist = open(sys.argv[2]).readlines()
    testlist = open(sys.argv[3]).readlines()
    relevant_dict = build_relevant_dict(sys.argv[4])

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
    MAP,PatN,Pat10 = evaluate(costlist, keywordlist, testlist, relevant_dict)
    print('MAP=%.3f PatN=%.3f Pat10=%.3f'%(MAP,PatN,Pat10))

