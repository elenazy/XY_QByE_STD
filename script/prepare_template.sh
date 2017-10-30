keyword_all_list=/home/disk1/jyhou/feats/XiaoYing_STD/list/keywords_60_100_50_all.list
random_num=5
for max_template_num in 1 2 4 8 12 16 24 32; 
do
    keyword_templatenum_randomnum_list=/home/disk1/jyhou/feats/XiaoYing_STD/list/keywords_60_100_50_${max_template_num}_XXX.list
    python script/prepare_template.py $keyword_all_list $max_template_num $random_num $keyword_templatenum_randomnum_list
done
