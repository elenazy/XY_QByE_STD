import sys
import numpy as np
intance_num=33
intance_num_list = [1,2,4,8,12,16,24,32]
            
if __name__=="__main__":
    if(len(sys.argv)<3):
        print("UDAGE: python "+ sys.argv[0]+ " out_log summery_file")
        exit(1)

    result_all = {}

    for line in open(sys.argv[1]).readlines():
        if line.find("/home/disk1/jyhou/feats/XiaoYing_STD") >= 0:
            fields = line.strip().split("/")
            keyword_field = fields[6]
            data_field = fields[7]
            
            fields = keyword_field.split("_")
            template_num = fields[5]
            random_num = fields[6]

            fields = data_field.split("_")
            data_type = "_".join(fields[-3:-1])
            if not result_all.has_key(keyword_field):
                result_all[keyword_field]=""
        elif line.find("unigram keyword") >= 0:
            fields = line.strip().split(" ")
            MAP = float(fields[2].strip().split("=")[1])
            PatN = float(fields[3].strip().split("=")[1])
            result_all[keyword_field] += "%.3f %.3f; "%(MAP,PatN)
        else:
            continue

    fid = open(sys.argv[2], "w")
    for keyword_field in result_all.keys():
        fid.writelines("%s: %s\n"%(keyword_field,result_all[keyword_field]))
