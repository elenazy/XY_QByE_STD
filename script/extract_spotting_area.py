import numpy as np
import sys
import wavedata
import random
import os

def relevant(query, text_id, relevant_dict):
    if text_id in relevant_dict[query]:
        return True
    return False

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

def extract_spotting_area(scorelist_all, arealist_all, querylist, doclist, relevant_dict):
    extract_list_all = []
    for i in range(len(querylist)):
        true_list=[]
        false_list=[]
        extract_list=[]
        ranklist = np.array(scorelist_all[i]).argsort()
        for j in range(len(ranklist)):
            j_r = ranklist[j]
            keyword_id = querylist[i].strip() 
            keyword = querylist[i].strip().split("_")[0]
            utt_id = doclist[j_r].strip()
            doc_id = "_".join(doclist[j_r].strip().split("_")[:-1])
            if relevant(keyword, doc_id, relevant_dict):
                true_list.append([ keyword_id, utt_id, 1, scorelist_all[i][j_r], j, arealist_all[i][j_r] ])
            else:
                false_list.append([ keyword_id, utt_id, 0, scorelist_all[i][j_r], j, arealist_all[i][j_r] ])
        true_num = len(true_list)
        extract_list = true_list + false_list[0:true_num]
        extract_list_all.append(extract_list)
    return extract_list_all

def frame_to_point(frame_pair):
    return (frame_pair[0]*10*8, frame_pair[1]*10*8+25*8) 


def write_spot_wave(extract_list_all, doc_scp, out_dir):
    doc_dic = {}
    for line in open(doc_scp).readlines():
        fields = line.strip().split()
        if len(fields) != 2:
            print("Error: the fields of doc scp file is not 2\n")
            exit(1)
        doc_id = fields[0]
        wav_path = fields[1]
        if doc_dic.has_key(doc_id):
            print("Error: repeat key in doc scp file\n")
        doc_dic[doc_id] = wav_path

        
    for extract_list in extract_list_all:
        keyword_id = extract_list[0][0]
        keyword_out_dir = out_dir + "-".join(keyword_id.split("'"))
        cmd = "mkdir -p " + keyword_out_dir
        os.system(cmd)
        for item in extract_list:
            doc_id = item[1]
            has_keyword = item[2]
            score = item[3]
            rank_position = item[4]
            extract_point = frame_to_point(item[5])
            inputfilename = doc_dic[doc_id]
            data = wavedata.readwave(inputfilename)
            spotting_data = data[extract_point[0]:extract_point[1]]
            outputfilename = keyword_out_dir + "/%s_%s_%s_%s_%s_%s_%s.wav"%(str(rank_position).zfill(4), str(has_keyword), str(score), str(extract_point[0]), str(extract_point[1]),keyword_id, doc_id)
            wavedata.writewave(outputfilename, spotting_data, 1, 2, 8000)

if __name__=="__main__":
    if len(sys.argv) < 7:
        print("USAGE: python %s result_dir keywordlist testlist testscp textfile ourdir"%sys.argv[0])
        exit(1)
    
    result_dir =  sys.argv[1]
    keywordlist = open(sys.argv[2]).readlines()
    testlist = open(sys.argv[3]).readlines()
    doc_scp_file = sys.argv[4]
    relevant_dict = build_relevant_dict(sys.argv[5])
    out_dir = sys.argv[6]

    scorelist_all = []
    arealist_all = []
    for keyword in keywordlist:
        result_fid = open(result_dir + keyword.strip() + ".RESULT")
        resultlist = result_fid.readlines()
        result_fid.close()
        
        scorelist = []
        arealist = []
        for res in resultlist:
            fields =res.strip().split()
            score = float(fields[0])
            start_point = int(fields[1])
            end_point = int(fields[2])
            scorelist.append(score)
            arealist.append((start_point, end_point))

        scorelist_all.append(scorelist)
        arealist_all.append(arealist)

    extract_list_all = extract_spotting_area(scorelist_all, arealist_all, keywordlist, testlist, relevant_dict)
    write_spot_wave(extract_list_all, doc_scp_file, out_dir)

