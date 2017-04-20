#!/usr/bin/bash
stage=1
fea_type="sbnf"
if [ $fea_type = "sbnf" ]; then
    distance_type="cosine"
    do_mvn=1;
fi

for x in  keywords_native_95_100; #keywords_95_100 keywords_75_80 keywords_55_60 keywords_native;
do
    keyword_dir="/mnt/jyhou/feats/XiaoYing_STD/$x/"
    average_dir="/mnt/jyhou/feats/XiaoYing_STD/a_${x}/"
    keyword_list_dir="/mnt/jyhou/feats/XiaoYing_STD/list/"
    keyword_list_basename="${x}_all.list"
    average_list_basename="${x}_average.list"
    keyword_list_file="${keyword_list_dir}${keyword_list_basename}"
    mkdir -p $average_dir
    
    #keyword_list_file="keyword_debug.list"
    if [ ! -f ${keyword_list_file} ]; then
        echo "ERROR: can not find the keyword list file: $keyword_list_file"
    fi
    
    if [ $stage -le 1 ]; then
        echo "./STD_v3/template_avg $keyword_dir ${keyword_list_file} $fea_type $distance_type $do_mvn $average_dir"
              ./STD_v3/template_avg $keyword_dir ${keyword_list_file} $fea_type $distance_type $do_mvn $average_dir
    fi

    find $average_dir -name *.$fea_type | sed -e "s:^${average_dir}::" -e "s:.${fea_type}$::" | sort > "${keyword_list_dir}${average_list_basename}"

done    
