# USAGE:python calculate_syllable_num.py keywordlist sylla_dict keyword_syllable_num
keywordlist=/mnt/jyhou/workspace/my_egs/xiaoying_all/s5c/data/info/keywords.list
sylla_dict=data/syll.dict
keyword_syllable_num=data/keyword_syllable_num.txt
echo "python script/calculate_syllable_num.py $keywordlist $sylla_dict $keyword_syllable_num"
python script/calculate_syllable_num.py $keywordlist $sylla_dict $keyword_syllable_num
