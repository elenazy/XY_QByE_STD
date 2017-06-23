# USAGE:python calculate_syllable_num.py keywordlist sylla_dict keyword_syllable_num
mkdir -p data
keywordlist=/home/disk1/jyhou/my_egs/swbd_xy_egs/info/keywords.list

sylla_dict=/home/disk1/jyhou/my_egs/swbd_xy_egs/info/syll.dict
keyword_syllable_num=data/keyword_syllable_num.txt
echo "python script/calculate_syllable_num.py $keywordlist $sylla_dict $keyword_syllable_num"
python script/calculate_syllable_num.py $keywordlist $sylla_dict $keyword_syllable_num
