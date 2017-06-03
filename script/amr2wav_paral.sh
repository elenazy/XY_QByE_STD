#!/bin/bash

echo "$0 $@"
echo ""

if [ $# != 7 ]; then
    echo "Udage: $0 <source_dir> <target_dir> <listfile> <source_type> <target_type> <log dir> <job number>"
    exit 1;
fi
source_dir=$1
target_dir=$2
listfile=$3
source_type=$4
target_type=$5
log_dir=$6
jb_num=$7
   
tmp_list_dir=`mktemp -d temp.XXXX`
mkdir -p ${log_dir}

python script/split.py $listfile $tmp_list_dir/ $jb_num 

list_file_base_name=`basename $listfile`

script/run.pl JOB=1:$jb_num $log_dir/convert_amr2wav.JOB.log \
    script/amr2wav.sh $source_dir $target_dir ${tmp_list_dir}/${list_file_base_name}JOB $source_type $target_type

rm -r $tmp_list_dir
