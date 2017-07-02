text_file="/home/disk1/jyhou/my_egs/swbd_xy_egs/info/text_fixed_tail_500"
keyword_list_dir="/home/disk1/jyhou/feats/XiaoYing_STD/list/"
data_list_dir="/home/disk1/jyhou/feats/XiaoYing_STD/list/"

keyword_type=keywords_60_100_10_1
keyword_dir="/home/disk1/jyhou/feats/XiaoYing_STD/a_${keyword_type}/"
keyword_list_basename="${keyword_type}_average.list"
keyword_list_file=${keyword_list_dir}${keyword_list_basename}

fea_type="sbnf1"
for x in data_15_30 data_40_55 data_65_80;
do
   result_dir=${keyword_dir}dtw_${x}_${fea_type}/
   test_list_file="${data_list_dir}/${x}.list"
   sr_result_file=/home/disk1/jyhou/my_code/XY_Text_STD/data/${x}.text
   echo $result_dir
   echo "python ./script/get_QbE_good_SR_bad.py $result_dir $keyword_list_file $test_list_file $text_file $sr_result_file"
         python ./script/get_QbE_good_SR_bad.py $result_dir $keyword_list_file $test_list_file $text_file $sr_result_file
done
