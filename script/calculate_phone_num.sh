# USAGE:python calculate_syllable_num.py keywordlist sylla_dict keyword_syllable_num
mkdir -p info/
keywordlist=/home/disk1/jyhou/my_egs/swbd_xy_egs/info/isolates.list

sylla_dict=/home/disk1/jyhou/my_egs/swbd_xy_egs/info/syll.dict
keyword_syllable_num=info/keyword_phone_num.txt
echo "python script/calculate_phone_num.py $keywordlist $sylla_dict $keyword_syllable_num"
python script/calculate_phone_num.py $keywordlist $sylla_dict $keyword_syllable_num
