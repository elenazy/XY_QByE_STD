stage=1
core_num=20
keyword_dir="/mnt/jyhou/feats/XiaoYing_STD/keyword/"
keyword_list_dir="/mnt/jyhou/feats/XiaoYing_STD/list/"
keyword_list_basename="keywords.list"
keyword_list_file=${keyword_list_dir}${keyword_list_basename}

test_list_file="/mnt/jyhou/feats/XiaoYing_STD/list/utterances.list"
text_file="/mnt/jyhou/workspace/my_egs/xiaoying_native/s5c/data/xiaoying_native/text"

fea_type="sbnf"

for x in data_55_60 data_75_80 data_95_100;
do
    result_dir=${keyword_dir}dtw_${x}_${fea_type}/
    test_scp_file="/mnt/jyhou/workspace/my_egs/xiaoying_std/s5c/data/$x/wav.scp"
    out_dir="/mnt/jyhou/data/spotting_result/dtw_${fea_type}_$x/"
    echo $result_dir
    echo "python extract_spotting_area.py $result_dir $keyword_list_file $test_list_file $test_scp_file $text_file $out_dir"
          python extract_spotting_area.py $result_dir $keyword_list_file $test_list_file $test_scp_file $text_file $out_dir
done


