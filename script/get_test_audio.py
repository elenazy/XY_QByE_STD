import sys
import numpy as np
from XiaoYingWave import XiaoYingWave
import json
import log

def build_wav_dict(text_file):
    wav_dict = {}
    text_list = open(text_file).readlines()
    for line in text_list:
        fields = line.strip().split()
        text_id = fields[0]
        text = " ".join(fields[1:])
        wav_dict[text_id] = XiaoYingWave(text_id, text)
    return wav_dict

def build_score_dict(jsonlistfile):
    score_dict = {}
    json_list = open(jsonlistfile).readlines()
    for line in json_list:
        fields = line.strip().split("/")
        text_id = "_".join(fields[-4:-2])
        time_stamp = fields[-2][-8:]
        if(not score_dict.has_key(text_id)):
            score_dict[text_id]={}
        json_items = open(line.strip()).readlines() 
        for json_item in json_items:
            json_entity = json.loads(json_item.strip())
            if json_entity.has_key("AudioName"):
                audio_id = str(json_entity["AudioName"])
            elif json_entity.has_key("audioName"):
                audio_id = str(json_entity["audioName"])
            else:
                log.Error("bad json file:%s"%json_item)
            
            if json_entity.has_key("Score"):
                score = float(json_entity["Score"])
            elif json_entity.has_key("score"):
                score = float(json_entity["score"])
            else:
                log.Error("bad json file:%s"%json_item)
            
            score_id = time_stamp + "_" + audio_id
            if score_dict[text_id].has_key(score_id):
                log.Error("repeated score_id: %s for text_id: %s"%(score_id, text_id))        
            score_dict[text_id][score_id] = score
    return score_dict

def set_wav(wav_dict, score_dict):
    for text_id in wav_dict.keys():
        if not score_dict.has_key(text_id):
            log.Error("we don't have audio for the text_id:%s"%text_id)

        for wav_id, score in score_dict[text_id].items():
            wav_dict[text_id].setWavList(wav_id, score)


def select_wav(wav_dict, score_low, score_high, num, output_dir):
    uttscpfid = open(output_dir + "/utter.list", "w")
    wavscpfid = open(output_dir + "/wav.scp", "w")
    textfid = open(output_dir + "/text", "w")
    for text_id in wav_dict:
        selected_wav_list = wav_dict[text_id].getWav(score_low, score_high, num)
        for i in range(len(selected_wav_list)):
            utt_id = text_id + "_" + str(i).zfill(2)
            text = wav_dict[text_id].getText()
            text_dir = "/".join(text_id.split("_"))
            utt_file = "SystemLogInfo" + "/".join(selected_wav_list[i].split("_")) 
            wav_file = "SystemLogInfo" + "/".join(selected_wav_list[i].split("_")) + ".wav"
            uttscpfid.writelines(text_dir + "/" + utt_file + "\n")
            wavscpfid.writelines(utt_id + " " + text_dir + "/" + wav_file + "\n")
            textfid.writelines(utt_id + " " + text + "\n")
    
if __name__=="__main__":
    if(len(sys.argv) < 7):
        print("USAGE: python " + sys.argv[0] + " text jsonfile.list score_low score_high num output_dir")
        exit(1)
    wav_dict = build_wav_dict(sys.argv[1])
    score_dict = build_score_dict(sys.argv[2])
    set_wav(wav_dict, score_dict)
    score_low = float(sys.argv[3])
    score_high = float(sys.argv[4])
    number = int(sys.argv[5])
    output_dir = sys.argv[6]
    select_wav(wav_dict, score_low, score_high, number, output_dir)
    
