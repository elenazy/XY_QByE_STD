import sys


if __name__=="__main__":
    if (len(sys.argv) < 3):
        print("USAGE:python %s text output"%sys.argv[0])
        exit(1)
    text_list = open(sys.argv[1]).readlines()
    fid = open(sys.argv[2], "w")
    words_dic = {}
    for line in text_list:
        fields = line.strip().split()
        text_id = fields[0]
        for word in fields[1:]:
            if not words_dic.has_key(word):
                words_dic[word]=0
            words_dic[word] += 1
    print(str(len(words_dic)))
    for key in words_dic.keys():
        fid.writelines("%s\t%d\n"%(key, words_dic[key]))
