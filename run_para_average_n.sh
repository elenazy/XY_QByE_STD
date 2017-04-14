#!/usr/bin/bash
stage=1
core_num=20
keyword_dir="/mnt/jyhou/feats/XiaoYing_STD/keyword_n/"
keyword_list_dir="/mnt/jyhou/feats/XiaoYing_STD/list/"
keyword_list_basename="keywords_n.list"
keyword_list_file=${keyword_list_dir}${keyword_list_basename}

test_list_file="/mnt/jyhou/feats/XiaoYing_STD/list/utterances.list"
ctm_file="/mnt/jyhou/workspace/my_egs/xiaoying_native/s5c/exp/nn_xiaoying_native_ali/ctm"

fea_type="sbnf"
if [ $fea_type = "sbnf" ]; then
    distance_type="cosine"
    do_mvn=1;
fi
#keyword_list_file="keyword_debug.list"
if [ ! -f ${keyword_list_file} ]; then
    echo "ERROR: can not find the keyword list file: $keyword_list_file"
fi

if [ $stage -le 1 ]; then
    mkdir -p ./tmp
    python script/split.py ${keyword_list_file} ./tmp/ ${core_num}
    
    for x in data_55_60 data_75_80 data_95_100;
    do
        test_dir="/mnt/jyhou/feats/XiaoYing_STD/$x/"
        result_dir=${keyword_dir}dtw_${x}_${fea_type}/;
            mkdir -p $result_dir
            for i in `seq $core_num`; do
            {
                echo "./STD_v3/dtw_std $keyword_dir ./tmp/${keyword_list_basename}${i} $test_dir $test_list_file $fea_type $distance_type $do_mvn $result_dir"
                      ./STD_v2/dtw_std $keyword_dir ./tmp/${keyword_list_basename}${i} $test_dir $test_list_file $fea_type $distance_type $do_mvn $result_dir
            } &
            done
            wait
    done
#rm -r ./tmp
fi

if [ $stage -le 2 ]; then
    for x in data_55_60 data_75_80 data_95_100;
    do
       result_dir=${keyword_dir}dtw_${x}_${fea_type}/
       echo $result_dir
       python evaluate.py $result_dir $keyword_list_file $test_list_file $ctm_file
    done
fi
