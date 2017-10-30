import sys

if __name__=="__main__":
    if len(sys.argv) < 4:
        print("USAGE:python %s keywords.list unigram.list bigram.list"%sys.argv[0])
        exit(1)
    keyword_list = open(sys.argv[1]).readlines()
    fid1=open(sys.argv[2],"w")
    fid2=open(sys.argv[3],"w")

    for word in keyword_list:
        if word.find("-") > 0:
            fid2.writelines(word.strip())
            fid2.writelines("\n")
        else:
            fid1.writelines(word.strip())
            fid1.writelines("\n")
           
    fid1.close();
    fid2.close() 
