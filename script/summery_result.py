import sys
import numpy as np

class Result():
    __search_data=None
    __map_results=[]
    __patn_results=[]
    __pat5_results=[]

    def __init__(self, search_data, template_num):
        self.__search_data = search_data
        self.__map_results=[]
        self.__patn_results=[]
        self.__pat5_results=[]
        for i in range(template_num):
            self.__map_results.append([])
            self.__patn_results.append([])
            self.__pat5_results.append([])

    def insert_result(self, template_id, MAP, PatN, Pat5):
        self.__map_results[template_id].append(MAP)
        self.__patn_results[template_id].append(PatN)
        self.__pat5_results[template_id].append(Pat5)

    def get_summery_out(self):
        print(str(self.__map_results))
        map_all = [np.mean(self.__map_results, 1), np.max(self.__map_results, 1), np.min(self.__map_results, 1)]
        patn_all = [np.mean(self.__patn_results, 1), np.max(self.__patn_results, 1), np.min(self.__patn_results, 1)]
        pat5_all = [np.mean(self.__pat5_results, 1), np.max(self.__pat5_results, 1), np.min(self.__pat5_results, 1)]

        return [map_all, patn_all, pat5_all]
            
if __name__=="__main__":
    if(len(sys.argv)<3):
        print("UDAGE: python "+ sys.argv[0]+ " out_log summery_file")
        exit(1)

    result_all = {}
    for data_type in ["15_30", "40_55", "65_80"]:
        result_all[data_type]=Result(data_type, 10)

    for line in open(sys.argv[1]).readlines():
        if line.find("/mnt/jyhou/feats/XiaoYing_STD") >= 0:
            fields = line.strip().split("/")
            keyword_field = fields[5]
            data_field = fields[6]
            
            fields = keyword_field.split("_")
            template_num = fields[4]
            random_num = fields[5]

            fields = data_field.split("_")
            data_type = "_".join(fields[2:4])
        elif line.find("all keyword") >= 0:
            fields = line.strip().split(" ")
            MAP = float(fields[2].strip().split("=")[1])
            PatN = float(fields[3].strip().split("=")[1])
            Pat5 = float(fields[4].strip().split("=")[1])
            result_all[data_type].insert_result(int(template_num)-1, MAP, PatN, Pat5)
        else:
            continue

    fid = open(sys.argv[2], "w")
    for data_type in result_all.keys():
        summery_result = result_all[data_type].get_summery_out()
        fid.writelines(data_type + "\n")
        for i in range(10):
            for j in range(3):
                for k in range(3):
                    fid.writelines("%f\t"%(summery_result[k][j][i]))
            fid.writelines("\n")
    fid.close()
