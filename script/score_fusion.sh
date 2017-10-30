fea_type="sbnf3"
feat_dir="/home/disk1/jyhou/feats/XiaoYing_STD"
keyword_list_dir="./info/"
data_list_dir="/home/disk1/jyhou/feats/XiaoYing_STD/list/"

text_file="/home/disk1/jyhou/my_egs/swbd_xy_egs/info/text_fixed_tail_500"
syllable_num_file="data/keyword_syllable_num.txt"

keyword_list_basename="unigram.list"
keyword_list_file=${keyword_list_dir}${keyword_list_basename}
keyword_dir="$feat_dir/at_keywords_60_100_50_32_5/"
#for factor in 0.5; do #0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9; do
##for factor in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9; do
##   echo $factor
#for x in data_15_30 data_40_55 data_65_80;
#do
#   result_dir1=${keyword_dir}i_dtw_${x}_${fea_type}/
#   result_dir2=/home/disk1/jyhou/my_egs/swbd_xy_egs/results/${x}_lattice/
#   fusion_dir=./results/${x}_fusion/
#   mkdir -p $fusion_dir
#
#   test_list_file="${data_list_dir}/${x}.list"
#   python ./script/score_fusion.py $keyword_list_file $result_dir1 $result_dir2  $factor $fusion_dir
#   echo $fusion_dir 
#   python ./script/evaluate.py $fusion_dir $keyword_list_file $test_list_file $text_file $syllable_num_file
#done
#done

keyword_type=keywords_60_100_50
hmm_type="h2"
transition_prob="0"
tempalte_num=32
random_num=5
global_variance=1
state_num_per_phone=9
mix_num=1
for factor in 0.5; do #0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9; do
#for factor in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9; do
   echo $factor
for x in data_15_30 data_40_55 data_65_80;
do
   keyword_dir1="${feat_dir}/hta_${keyword_type}_${tempalte_num}_${random_num}_${hmm_type}_${global_variance}_${transition_prob}_${state_num_per_phone}_${mix_num}/"
   result_dir1=${keyword_dir1}hta_i_viterbi_${x}_${fea_type}/
   keyword_dir2="/home/disk1/jyhou/my_egs/swbd_xy_egs/results/"
   result_dir2=${keyword_dir2}/${x}_lattice/
   fusion_dir=./results/${x}_fusion/
   mkdir -p $fusion_dir

   test_list_file="${data_list_dir}/${x}.list"
   python ./script/score_fusion.py $keyword_list_file $result_dir1 $result_dir2  $factor $fusion_dir
   echo $fusion_dir 
   python ./script/evaluate.py $fusion_dir $keyword_list_file $test_list_file $text_file $syllable_num_file
done
done
