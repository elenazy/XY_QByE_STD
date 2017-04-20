#!/bin/bash
# python get_test_audio.pytext wavfile.list jsonfile.list score_low score_high output_dir
. ./copy.sh
stage=0
if [ $stage -le 0 ]; then
    for x in data_95_100 data_75_80 data_55_60; 
    do
        cat /mnt/jyhou/workspace/my_egs/xiaoying_std/s5c/data/local/$x/utter.list || exit 1;
    done > exclude.list
    
    for x in data_95_100 data_75_80 data_55_60;
    do
        cat /mnt/jyhou/workspace/my_egs/xiaoying_non-native/s5c/data/local/$x/utter.list || exit 1;
    done >> exclude.list
fi

if [ $stage -le 1 ]; then
    text=/mnt/jyhou/workspace/my_egs/xiaoying_native/s5c/data/xiaoying_native/text
    jsonfile=/mnt/jyhou/data/userTextAudio/json.list
    exclude_list=exclude.list

    score_low=45
    score_high=100
    output_dir=/mnt/jyhou/workspace/my_egs/xiaoying_non-native/s5c/data/local/train
    mkdir -p $output_dir
    python get_train_audio.py $text $jsonfile $exclude_list $score_low $score_high 300 $output_dir

fi

if [ $stage -le 2 ]; then
    for x in train;
    do
        source_dir=/mnt/jyhou/data/userTextAudio
        target_dir=/mnt/jyhou/data/XiaoYing_Train/$x
        output_dir=/mnt/jyhou/workspace/my_egs/xiaoying_non-native/s5c/data/local/$x
        coping $source_dir $target_dir $output_dir/utter.list "amr" "amr"
        ./amr2wav_paral.sh $target_dir $target_dir $output_dir/utter.list "amr" "wav" ./log/ 20
    done
fi
