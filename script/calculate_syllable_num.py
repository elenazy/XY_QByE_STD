import sys

def build_syllable_dictionary(dictionary_file):
    syllable_num_dict = {}
    for line in open(dictionary_file).readlines():
        fields = line.strip().split()
        word_id = fields[0]
        syll_fields = fields[1].split("-")
        syllable_num_dict[word_id]=len(syll_fields)
    return syllable_num_dict

if __name__=="__main__":
    if (len(sys.argv) < 4):
        print("USAGE:python %s keywordlist sylla_dict keyword_syllable_num"%(sys.argv[0]))
        exit(1)
    keyword_list = []
    for line in open(sys.argv[1]).readlines():
        keyword_list.append(line.strip().split("_")[0])   
    #build syllable dictionaty
    syllable_num_dict = build_syllable_dictionary(sys.argv[2])

    fid = open(sys.argv[3], "w")
    for keyword in keyword_list:
        keyword_uppercase = keyword.upper()
        num = -1
        if syllable_num_dict.has_key(keyword_uppercase):
            num = syllable_num_dict[keyword_uppercase]
        fid.writelines("%s %d\n"%(keyword, num))
    fid.close()
