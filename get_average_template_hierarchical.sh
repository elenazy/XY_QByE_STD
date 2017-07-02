#!/bin/bash
stage=1
fea_type="sbnf1"

if [ $fea_type = "sbnf1" ]; then
    distance_type="cosine"
    do_mvn=1;
fi

feat_dir=/home/disk1/jyhou/feats/XiaoYing_STD

for x in keywords_60_100;
do
    for tempalte_num in `seq 2 10`;
    do
        for random_num in `seq 5`;
        do
            keyword_dir="$feat_dir/$x/"
            average_dir="$feat_dir/ah2_${x}_${tempalte_num}_${random_num}/"
            keyword_list_dir="${feat_dir}/list/"
            keyword_list_basename="${x}_${tempalte_num}_${random_num}.list"
            average_list_basename="${x}_${tempalte_num}_${random_num}_average.list"
            keyword_list_file="${keyword_list_dir}${keyword_list_basename}"
            mkdir -p $average_dir
            
            #keyword_list_file="keyword_debug.list"
            if [ ! -f ${keyword_list_file} ]; then
                echo "ERROR: can not find the keyword list file: $keyword_list_file"
            fi
            
            if [ $stage -le 1 ]; then
                echo "./STD_v3/template_avg_hierarchical $keyword_dir ${keyword_list_file} $fea_type $distance_type $do_mvn $average_dir"
                      ./STD_v3/template_avg_hierarchical $keyword_dir ${keyword_list_file} $fea_type $distance_type $do_mvn $average_dir
            fi
            find $average_dir -name *.$fea_type | sed -e "s:^${average_dir}::" -e "s:.${fea_type}$::" | sort > "${keyword_list_dir}${average_list_basename}"
        
        done
    done
done
