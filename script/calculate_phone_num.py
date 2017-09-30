import sys
import re

def build_phone_num_dictionary(dictionary_file):
    phone_num_dict = {}
    for line in open(dictionary_file).readlines():
        fields = line.strip().split()
        word_id = fields[0]
        phone_fields = re.split('\.|-', fields[1])
        phone_num_dict[word_id]=len(phone_fields)
    return phone_num_dict

def get_phone_num_of_keyword(syllable_num_dict, keyword):
    keyword_uppercase = keyword.upper()
    if (keyword_uppercase.find("-") >= 0):
        words = keyword_uppercase.split("-")
        num = syllable_num_dict[words[0]] + syllable_num_dict[words[1]]
    else:
        num = syllable_num_dict[keyword_uppercase]
    return num

if __name__=="__main__":
    if (len(sys.argv) < 4):
        print("USAGE:python %s keywordlist sylla_dict keyword_syllable_num"%(sys.argv[0]))
        exit(1)
    keyword_list = []
    for line in open(sys.argv[1]).readlines():
        keyword_list.append(line.strip().split("_")[0])   
    #build syllable dictionaty
    phone_num_dict = build_phone_num_dictionary(sys.argv[2])

    fid = open(sys.argv[3], "w")
    for keyword in keyword_list:
        new_keyword = "-".join(keyword.strip().split())
        num = get_phone_num_of_keyword(phone_num_dict, new_keyword)
        fid.writelines("%s %d\n"%(new_keyword, num))
    fid.close()
