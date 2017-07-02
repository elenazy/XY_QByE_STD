import numpy as np
import sys

def relevant(query, text_id, occurance_dict):
    if query in occurance_dict[text_id]:
        return True
    return False

def build_occurance_dict(keywords_list, text_file):
    keywords_list_uniq = set()
    for keyword in keywords_list:
        keywords_list_uniq.add(keyword.strip().split("_")[0])
    occurance_dict = {}
    for line in open(text_file).readlines():
        fields = line.strip().split()
        text_id = fields[0]
        single_words = fields[1:]
        occurance_dict[text_id] = set()
        for i in range(len(single_words)):
            if single_words[i] in keywords_list_uniq:
                occurance_dict[text_id].add(single_words[i])

        for i in range(len(single_words)-1):
            word1 = single_words[i]
            word2 = single_words[i+1]
            phrase = word1 + "-" + word2
            if phrase in keywords_list_uniq:
                occurance_dict[text_id].add(phrase)
    return occurance_dict

def write_pair_list(pair_list, out_file):
    fid = open(out_file, "w")
    for i in range(len(pair_list)):
        fid.writelines("%f %f\n"%(pair_list[i][0],pair_list[i])[1])

def build_dict(textfile):
    text_dict = {}
    for line in open(textfile).readlines():
        wav_id = line.strip().split()[0]
        text = " ".join(line.strip().split()[1:])
        text_dict[wav_id] = text
    return text_dict

def get_qbe_good_sr_bad(finalScore):
    Ntotal = len(finalScore)
    qbegoodsrbad_num =0;
    qbegoodsrgood_num = 0;
    qbebadsrgood_num = 0;
    sortedFinalScore=sorted(finalScore, key=lambda t:t[0], reverse = True)
    for i in range(Ntotal):
        if (sortedFinalScore[i][1] and not sortedFinalScore[i][2]):
            print("QbE good and SR bad: score: %f, keyword: %s, utterance: %s\n"%(sortedFinalScore[i][0], sortedFinalScore[i][3], sortedFinalScore[i][4]))
            print("trans: %s\n"%sortedFinalScore[i][5])
            print("sr: %s\n"%sortedFinalScore[i][6])
            qbegoodsrbad_num +=1
        #elif (sortedFinalScore[i][1] and sortedFinalScore[i][2]):
        #    print("QbE good and SR good: score: %f, keyword: %s, utterance: %s\n"%(sortedFinalScore[i][0], sortedFinalScore[i][3], sortedFinalScore[i][4]))
        #    print("trans: %s\n"%sortedFinalScore[i][5])
        #    print("sr: %s\n"%sortedFinalScore[i][6])
        #    qbegoodsrgood_num +=1
        #elif (not sortedFinalScore[i][1] and sortedFinalScore[i][2]):
        #    print("QbE good and SR good: score: %f, keyword: %s, utterance: %s\n"%(sortedFinalScore[i][0], sortedFinalScore[i][3], sortedFinalScore[i][4]))
        #    print("trans: %s\n"%sortedFinalScore[i][5])
        #    print("sr: %s\n"%sortedFinalScore[i][6])
        #    qbebadsrgood_num +=1
        else:
            continue

    print("qbegoodsrbad_num: %d, qbegoodsrgood_num: %d, qbebadsrgood_num: %d"%(qbegoodsrbad_num,qbegoodsrgood_num,qbebadsrgood_num))
if __name__=="__main__":
    if len(sys.argv) < 6:
        print("USAGE: python %s result_dir keywordlist testlist textfile recognition_result"%sys.argv[0])
        exit(1)
    
    result_dir =  sys.argv[1]
    keyword_list = open(sys.argv[2]).readlines()
    test_list = open(sys.argv[3]).readlines()
    occurance_dict_real = build_occurance_dict(keyword_list, sys.argv[4])
    occurance_dict_test = build_occurance_dict(keyword_list, sys.argv[5])
    text_dict = build_dict(sys.argv[4])
    recognition_dict = build_dict(sys.argv[5])

    cost_list_all = []
    real_num = 0 
    for i in range(len(keyword_list)):
        keyword = keyword_list[i]
        result_list = open(result_dir + keyword.strip() + ".RESULT").readlines()
        keyword_id = keyword.strip().split("_")[0]

        cost_list = []
        real = []
        test = []
        for j in range(len(test_list)):
            res = result_list[j]
            score = float(res.strip().split()[0])
            cost_list.append(1-score)
            
            doc_id = "_".join(test_list[j].strip().split("_")[:-1])
            if relevant(keyword_id, doc_id, occurance_dict_real):
                real.append(True)
                real_num += 1
            else:
                real.append(False)

            if relevant(keyword_id, test_list[j].strip(), occurance_dict_test):
                test.append(True)
            else:
                test.append(False)
        #norm_cost_list = evaluate.m_norm(cost_list)
        norm_cost_list = cost_list
        for j in range(len(test_list)):
            doc_id = "_".join(test_list[j].strip().split("_")[:-1])
            cost_list_all.append((norm_cost_list[j], real[j], test[j], keyword_id, test_list[j].strip(), text_dict[doc_id], recognition_dict[test_list[j].strip()]))

    print("occur num: %d, total num: %d \n"%(real_num, len(cost_list_all)))
    get_qbe_good_sr_bad(cost_list_all)
