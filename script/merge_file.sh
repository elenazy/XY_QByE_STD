#!/bin/bash

feature_type="sbnf"
keyword_list_dir="/mnt/jyhou/feats/XiaoYing_STD/list/"
keyword_list_basename_1="keywords_95_100_average.list"
keyword_list_file_1=${keyword_list_dir}${keyword_list_basename_1}

keyword_list_basename_2="keywords_native_average.list"
keyword_list_file_2=${keyword_list_dir}${keyword_list_basename_1}

keyword_dir_1="/mnt/jyhou/feats/XiaoYing_STD/a_keywords_native"
keyword_dir_2="/mnt/jyhou/feats/XiaoYing_STD/a_keywords_95_100"

merge_dir="/mnt/jyhou/feats/XiaoYing_STD/keywords_native_95_100"
keyword_list_basename_merge=keywords_native_95_100_all.list
mkdir -p $merge_dir
for file in `cat $keyword_list_file_1`;
do
    source_file=$file
    target_file=${file/_n/_1}
    cp ${keyword_dir_1}/${source_file}.${feature_type} \
        ${merge_dir}/${target_file}.${feature_type}

done

for file in `cat $keyword_list_file_2`;
do
    source_file=$file
    target_file=${file/_n/_2}
    cp ${keyword_dir_2}/${source_file}.${feature_type} \
        ${merge_dir}/${target_file}.${feature_type}

done

find $merge_dir -name *.$feature_type | sed -e "s:^${merge_dir}/::" -e "s:.${feature_type}$::" | sort > "${keyword_list_dir}${keyword_list_basename_merge}"
