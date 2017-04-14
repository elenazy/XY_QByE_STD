import sys
import log
import random

class XiaoYingWave():
    __text_id=None
    __text=None
    __wav_list=None
    
    def __init__(self, text_id, text):
        self.__text_id = text_id
        self.__text = text

    def initWavList(self, wav_list):
        self.__wav_list = wav_list

    def getTextId(self):
        return self.__text_id

    def getText(self):
        return self.__text

    def getWavList(self):
        return self.__wav_list

    def setWavList(self, wav_id, wav_score):
        if(self.__wav_list == None):
            self.__wav_list={}
        self.__wav_list[wav_id] = float(wav_score)

    def getWav(self, lowscore, highscore, num):
        if(self.__wav_list==None):
           log.Error("wav-score list is null")
       
        wav_id_list=[]
        i=0
        while len(wav_id_list) < num:
            wav_id_list=[]
            for (wav_id, score) in self.__wav_list.items():
                if(score > lowscore and score < highscore):
                    wav_id_list.append(wav_id)
            lowscore -= 2
            highscore +=2
            i += 1
        if i > 1:
           log.Log("retry %d times for sentence %s"%(i-1, self.__text_id)) 
        if len(wav_id_list) < num:
           log.Error("not enough wav file meet the requirment of score, has: %d, require: %d"%(len(wav_id_list), num))
        return random.sample(wav_id_list, num) 
