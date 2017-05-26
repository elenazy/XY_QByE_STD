keyword_all_list=/mnt/jyhou/feats/XiaoYing_STD/list/keywords_60_100_all.list
random_num=5
for max_template_num in `seq 10`; 
do
    keyword_templatenum_randomnum_list=/mnt/jyhou/feats/XiaoYing_STD/list/keywords_60_100_${max_template_num}_XXX.list
    python script/prepare_template.py $keyword_all_list $max_template_num $random_num $keyword_templatenum_randomnum_list
done
