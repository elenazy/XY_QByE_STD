#!/bin/bash

feature_type="sbnf6"
keyword_list_dir="/mnt/jyhou/feats/XiaoYing_STD/list/"
keyword_list_basename_1="keywords_20_60_average.list"
keyword_list_file_1=${keyword_list_dir}${keyword_list_basename_1}

keyword_list_basename_2="keywords_native_average.list"
keyword_list_file_2=${keyword_list_dir}${keyword_list_basename_1}

keyword_dir_1="/mnt/jyhou/feats/XiaoYing_STD/a_keywords_native"
keyword_dir_2="/mnt/jyhou/feats/XiaoYing_STD/a_keywords_20_60"

merge_dir="/mnt/jyhou/feats/XiaoYing_STD/keywords_native-keywords_20_60"
keyword_list_basename_merge=keywords_native-keywords_20_60_all.list
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

#keyword_list_dir="/mnt/jyhou/feats/XiaoYing_STD/list/"
#
#keyword_list_basename_1="keywords_20_60_average.list"
#keyword_list_file_1=${keyword_list_dir}${keyword_list_basename_1}
#
#keyword_list_basename_2="keywords_60_100_average.list"
#keyword_list_file_2=${keyword_list_dir}${keyword_list_basename_1}
#
#keyword_list_basename_3="keywords_native_average.list"
#keyword_list_file_3=${keyword_list_dir}${keyword_list_basename_1}
#
#keyword_dir_1="/mnt/jyhou/feats/XiaoYing_STD/a_keywords_20_60"
#keyword_dir_2="/mnt/jyhou/feats/XiaoYing_STD/a_keywords_60_100"
#keyword_dir_3="/mnt/jyhou/feats/XiaoYing_STD/a_keywords_native"
#
#merge_dir="/mnt/jyhou/feats/XiaoYing_STD/keywords_all_type"
#keyword_list_basename_merge=keywords_all_type_all.list
#mkdir -p $merge_dir
#for file in `cat $keyword_list_file_1`;
#do
#    source_file=$file
#    target_file=${file/_n/_1}
#    cp ${keyword_dir_1}/${source_file}.${feature_type} \
#        ${merge_dir}/${target_file}.${feature_type}
#
#done
#
#for file in `cat $keyword_list_file_2`;
#do
#    source_file=$file
#    target_file=${file/_n/_2}
#    cp ${keyword_dir_2}/${source_file}.${feature_type} \
#        ${merge_dir}/${target_file}.${feature_type}
#
#done
#
#for file in `cat $keyword_list_file_3`;
#do
#    source_file=$file
#    target_file=${file/_n/_3}
#    cp ${keyword_dir_3}/${source_file}.${feature_type} \
#        ${merge_dir}/${target_file}.${feature_type}
#
#done
#
#find $merge_dir -name *.$feature_type | sed -e "s:^${merge_dir}/::" -e "s:.${feature_type}$::" | sort > "${keyword_list_dir}${keyword_list_basename_merge}"
