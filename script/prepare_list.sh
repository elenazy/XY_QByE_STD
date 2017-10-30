#!/bin/bash
mkdir -p list

for x in data_15_30  data_40_55  data_65_80  keywords_60_100_50;
do
    find $x -name *.sbnf3|sed -e "s:^$x/::" -e "s:.sbnf3$::"|sort > list/${x}_all.list
done
