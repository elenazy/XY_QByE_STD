import sys
import numpy as np
def m_norm(scorelist):
    hist, bin_edges = np.histogram(scorelist,40)
    index = hist.argmax();

    peak = (bin_edges[index] + bin_edges[index+1])/2

    slist_peak = np.array([x for x in scorelist if x >= peak])
    scorelist = (scorelist - peak)/slist_peak.std()

    return scorelist
    

def z_norm(scorelist):
    #scorelist = (np.array(scorelist)-min(scorelist))/(max(scorelist)-min(scorelist))
    mean = np.mean(scorelist)
    std  = np.std(scorelist)
    print std
    scorelist = (np.array(scorelist)-mean)/std
    return scorelist

def min_max_norm(scorelist):
    min_v = min(scorelist)
    max_v = max(scorelist)

    if (max_v-min_v)>0.00001:
        norm_scorelist = (np.array(scorelist)-min_v)/(max_v-min_v)
    else:
        max_v-min_v
        norm_scorelist = np.array(scorelist)
    return norm_scorelist

def get_score_all_list(result_dir, keyword_list):
    score_all_list = []
    for keyword in keyword_list:
        result_fid = open(result_dir + keyword.strip() + ".RESULT")
        result_list = result_fid.readlines()
        result_fid.close()
        
        score_list = []
        for res in result_list:
            score = float(res.strip().split()[0])
            score_list.append(score)
        score_all_list.append(score_list)
    return score_all_list

def fusion(score_all_list1, score_all_list2, factor):
    if len(score_all_list1) != len(score_all_list2):
        print("Error: bad length of score list")
    fusion_score_all_list = []
    for i in range(len(score_all_list1)): 
        #norm_score_list1 = m_norm(score_all_list1[i])
        #norm_score_list2 = m_norm(score_all_list2[i])
        norm_score_list1 = min_max_norm(score_all_list1[i])
        norm_score_list2 = min_max_norm(score_all_list2[i])
        fusion_score_list = []
        for j in range(len(norm_score_list1)):
            #if norm_score_list2[j] > 1: 
            #    fusion_score_list.append(norm_score_list1[j])
            #else:
            #    fusion_score_list.append(factor*norm_score_list1[j]+(1-factor)*norm_score_list2[j])
            fusion_score_list.append(factor*norm_score_list1[j]+(1-factor)*norm_score_list2[j])
        fusion_score_all_list.append(fusion_score_list) 
    return fusion_score_all_list

if __name__=="__main__":
    if len(sys.argv) < 6:
        print("UDAGE: python "+ sys.argv[0]+ "keyword_list_file result_dir1 result_dir2 fusion_dir")
        exit(1)
    
    keyword_list = open(sys.argv[1]).readlines()
    result_dir1 =  sys.argv[2]
    result_dir2 =  sys.argv[3]
    factor = float(sys.argv[4])
    fusion_dir = sys.argv[5]

    score_all_list1 = get_score_all_list(result_dir1, keyword_list)
    score_all_list2 = get_score_all_list(result_dir2, keyword_list)

    fusion_score_all_list = fusion(score_all_list1, score_all_list2, factor)

    for i in range(len(keyword_list)):
        fid = open(fusion_dir + keyword_list[i].strip() + ".RESULT","w")
        for x in fusion_score_all_list[i]:
            fid.writelines("%f\n"%x)
        fid.close()

