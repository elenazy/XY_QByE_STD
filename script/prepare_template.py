import sys
import os
import random

def sampling(source_list_dict, select_num):
    selected_list_dict={}
    for keyword in source_list_dict.keys():
        actual_num = min(len(source_list_dict[keyword]), select_num)
        selected_list = random.sample(source_list_dict[keyword], actual_num)
        selected_list_dict[keyword] = selected_list
    return selected_list_dict

def mkdir(path):
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)

def get_file(path, suffix):
    file_list = []
    items = os.listdir(path)
    for x in items:
        if os.path.isfile(path + "/" + x) and x.endswith(suffix):
            file_list.append(path + "/" + x)
            #print(path + "/" + x)
        elif os.path.isdir(path + "/" + x):
            file_list += get_file(path + "/" + x, suffix)
    return file_list

if __name__=="__main__":
    if(len(sys.argv)<3):
        print("UDAGE: python "+ sys.argv[0]+ " keyword_all_list_file  max_template_num  random_num  keyword_selected_list_file")
        exit(1)    

    source_list_file = sys.argv[1]
    select_num = int(sys.argv[2])
    random_num = int(sys.argv[3])
    selected_list_file_fake = sys.argv[4]

    source_list_dict = {}
    for item in open(source_list_file).readlines():
        keyword = item.strip().split("_")[0]
        if not source_list_dict.has_key(keyword):
            source_list_dict[keyword] = []
        source_list_dict[keyword].append(item)

    #for keyword in source_list_dict.keys():
    #    print("%s %d\n"%(keyword, len(source_list_dict[keyword])))

    for i in range(1, random_num+1):
        selected_list_dict = sampling(source_list_dict, select_num)
        selected_list_file_real = selected_list_file_fake.replace("XXX", str(i))
        fid = open(selected_list_file_real, "w")
        for keyword in selected_list_dict.keys():
            for item in selected_list_dict[keyword]:
                fid.writelines(item)
        fid.close()

