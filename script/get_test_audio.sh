#!/bin/bash
# python get_test_audio.pytext wavfile.list jsonfile.list score_low score_high output_dir
. ./copy.sh
stage=2

if [ $stage -le 1 ]; then
    text=/mnt/jyhou/workspace/my_egs/xiaoying_native/s5c/data/xiaoying_native/text
    jsonfile=/mnt/jyhou/data/userTextAudio/json.list
    
    score_low=95
    score_high=100
    output_dir=/mnt/jyhou/workspace/my_egs/xiaoying_std/s5c/data/local/data_95_100
    mkdir -p $output_dir
    python get_test_audio.py $text $jsonfile $score_low $score_high 2 $output_dir 
    
    score_low=75
    score_high=80
    output_dir=/mnt/jyhou/workspace/my_egs/xiaoying_std/s5c/data/local/data_75_80
    mkdir -p $output_dir
    python get_test_audio.py $text $jsonfile $score_low $score_high 2 $output_dir 
    
    
    score_low=55
    score_high=60
    output_dir=/mnt/jyhou/workspace/my_egs/xiaoying_std/s5c/data/local/data_55_60
    mkdir -p $output_dir
    python get_test_audio.py $text $jsonfile $score_low $score_high 2 $output_dir 

fi

if [ $stage -le 2 ]; then
    for x in data_95_100 data_75_80 data_55_60;
    do
        source_dir=/mnt/jyhou/data/userTextAudio
        target_dir=/mnt/jyhou/data/XiaoYing_STD/$x
        output_dir=/mnt/jyhou/workspace/my_egs/xiaoying_std/s5c/data/local/$x
        coping $source_dir $target_dir $output_dir/utter.list "amr" "amr"
        ./amr2wav.sh $target_dir $target_dir $output_dir/utter.list "amr" "wav"
    done
fi
