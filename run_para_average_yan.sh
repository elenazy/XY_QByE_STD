#!/usr/bin/bash
stage=1
core_num=4
    
keyword_list_dir="/home/disk1/jyhou/test/casesfromxiayan/list/"
data_list_dir="/home/disk1/jyhou/test/casesfromxiayan/list/"

fea_type="sbnf1"

if [ $fea_type = "sbnf1" ]; then
    distance_type="cosine"
    do_mvn=1;
fi
#for x in keywords_20_60 keywords_60_100 keywords_native keywords_native-keywords_60_100;
fea_dir=/home/disk1/jyhou/test/casesfromxiayan
for x in keywords
do
    keyword_dir="${fea_dir}/at_${x}/"
    keyword_list_basename="${x}_average.list"
    keyword_list_file=${keyword_list_dir}${keyword_list_basename}
    
    #keyword_list_file="keyword_debug.list"
    if [ ! -f ${keyword_list_file} ]; then
        echo "ERROR: can not find the keyword list file: $keyword_list_file"
    fi
    
    if [ $stage -le 1 ]; then
        for x in tests;
        do
            test_dir="$fea_dir/$x/"
            test_list_file="${data_list_dir}/${x}.list"
            result_dir=${keyword_dir}dtw_${x}_${fea_type}/;
            mkdir -p $result_dir
            echo "./STD_v3/dtw_std $keyword_dir ${keyword_list_file} $test_dir $test_list_file $fea_type $distance_type $do_mvn $result_dir"
                  #./STD_v3/dtw_std $keyword_dir ${keyword_list_file} $test_dir $test_list_file $fea_type $distance_type $do_mvn $result_dir
        done
    fi
done
