#!/bin/bash

echo "$0 $@"
echo ""

if [ $# != 5 ]; then
    echo "Udage: $0 <source_dir> <target_dir> <listfile> <source type> <target type>"
    exit 1;

fi

source_dir=$1
target_dir=$2
listfile=$3
source_type=$4
target_type=$5

for filename in `cat $listfile`; 
do
  echo "ffmpeg -i $source_dir/${filename}.${source_type} -y -r $target_dir/${filename}.${target_type}"
  ffmpeg -i $source_dir/${filename}.${source_type} -ac 1 -ar 8000 -y $target_dir/${filename}.${target_type}
done
