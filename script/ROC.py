import numpy as np
import sys
import evaluate

def write_pair_list(pair_list, out_file):
    fid = open(out_file, "w")
    for i in range(len(pair_list)):
        fid.writelines("%f %f\n"%(pair_list[i][0],pair_list[i])[1])

def ROC(finalScore, trueNum):
    Ntotal = len(finalScore)
    Nactual = trueNum
    Nmiss = Nactual
    Nfa = 0
    sortedFinalScore=sorted(finalScore, key=lambda t:t[0], reverse = True)
    fid=open("sorted_score.txt","w")
    for i in range(len(sortedFinalScore)):
        fid.writelines(str(sortedFinalScore[i]))
        fid.writelines("\n")
    Pfa_Pmiss=[]
    Pfa_Pmiss.append((0.0, 1.0))
    for i in range(Ntotal):
        if(sortedFinalScore[i][1]):
            Nmiss -=1
        else:
            Nfa +=1
        Pfa_Pmiss.append((Nfa/float(Ntotal-Nactual), Nmiss/float(Nactual)))
    return Pfa_Pmiss

if __name__=="__main__":
    if len(sys.argv) < 6:
        print("USAGE: python %s result_dir keywordlist testlist textfile ROC_file"%sys.argv[0])
        exit(1)
    
    result_dir =  sys.argv[1]
    keyword_list = open(sys.argv[2]).readlines()
    test_list = open(sys.argv[3]).readlines()
    occurance_dict = evaluate.build_occurance_dict(keyword_list, sys.argv[4])

    cost_list_all = []
    real_num = 0 
    for i in range(len(keyword_list)):
        keyword = keyword_list[i]
        result_list = open(result_dir + keyword.strip() + ".RESULT").readlines()

        cost_list = []
        real = []
        for j in range(len(test_list)):
            res = result_list[j]
            score = float(res.strip().split()[0])
            cost_list.append(1 - score)
            
            keyword_id = keyword.strip().split("_")[0]
            doc_id = "_".join(test_list[j].strip().split("_")[:-1])
            if evaluate.relevant(keyword_id, doc_id, occurance_dict):
                real.append(True)
                real_num += 1
            else:
                real.append(False)
        norm_cost_list = evaluate.m_norm(cost_list)
        norm_cost_list = cost_list
        for j in range(len(test_list)):
            cost_list_all.append((norm_cost_list[j], real[j]))

    Pfa_Pmiss = ROC(cost_list_all, real_num) 
    write_pair_list(Pfa_Pmiss, sys.argv[5])
