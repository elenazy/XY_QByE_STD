#!/usr/bin/bash
stage=1
keyword_dir="/mnt/jyhou/feats/XiaoYing_STD/keyword/"
keyword_list_dir="/mnt/jyhou/feats/XiaoYing_STD/list/"
keyword_list_basename="keywords.list"
keyword_list_file="${keyword_list_dir}${keyword_list_basename}"
out_dir="/mnt/jyhou/feats/XiaoYing_STD/keyword_n/"
mkdir -p $out_dir

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
    echo "./STD_v3/template_avg $keyword_dir ${keyword_list_file} $fea_type $distance_type $do_mvn $out_dir"
          ./STD_v3/template_avg $keyword_dir ${keyword_list_file} $fea_type $distance_type $do_mvn $out_dir
fi

