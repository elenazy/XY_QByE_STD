#!/bin/bash
mkdir list

for x in data_15_30  data_40_55  data_65_80  keywords_60_100  keywords_native;
do
    find $x -name *.sbnf1|sed -e "s:^$x/::" -e "s:.sbnf1$::"|sort > list/${x}_all.list
done
