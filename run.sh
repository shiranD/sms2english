#! /bin/sh

#Created on May 26 2017

#@author: Shiran Dudy
#---------
#This shell script is the main script to run in order to have the data alined and trained with one of the proposed models. Aligning the data is optional and the models can be set as well.
#The script assumes keras environment under tensorflow

# Determine your input files of paralell corpus
path2sms=../../preprocess/new_sms2.txt
path2en=../../preprocess/new_en2.txt
# apply edit distance alignenmet
edit='intruc'

# make dirs
dir='db'
model_dir='models'
results_dir='model_eval'
mkdir -p $dir
mkdir -p $model_dir
mkdir -p $results_dir
mkdir -p imgs

# align data
if [ $edit == 'align' ]; then
  # edit.py aligns the data and process_edit.py split it to 2 corpuses
  # it generate db folder with the output of both sms and english texts
  echo '---------------------------'
  echo 'Align sms to english corpus'
  echo '---------------------------'
  python3 preprocess/edit.py $path2sms $path2en > $dir/out
  echo '---------------------------------------'
  echo 'Split to seperate sms and english files'
  echo '---------------------------------------'
  cat $dir/out | python preprocess/process_edit.py $dir
  #split_DB.py splits the corpuses to 5 folds and extract the number of unique symbols for each of the corpuses
  echo '---------------'
  echo 'Five Fold Split'
  echo '---------------'
  python aligned_corpus/split_DB.py $dir 1 | grep -oh '[0-9][0-9]*' > sym_count

elif [ $edit == 'intruc' ]; then
  # edit.py aligns the data and process_edit.py split it to 2 corpuses
  # it generate db folder with the output of both sms and english texts
  echo '---------------------------'
  echo 'Align sms to english corpus'
  echo '---------------------------'
  python3 preprocess/edit.py $path2sms $path2en > $dir/out
  echo '---------------------------------------'
  echo 'Split to seperate sms and edit intruction files'
  echo '---------------------------------------'
  cat $dir/out | python preprocess/process_op.py $dir
  #split_DB.py splits the corpuses to 5 folds and extract the number of unique symbols for each of the corpuses
  echo '---------------'
  echo 'Five Fold Split'
  echo '---------------'
  python aligned_corpus/split_DB.py $dir 0 | grep -oh '[0-9][0-9]*' > sym_count

else
  python preprocess/non_algn_preprocess.py $path2sms $path2en $dir
  #split_DB.py splits the corpuses to 5 folds and extract the number of unique symbols for each of the corpuses
  echo '---------------'
  echo 'Five Fold Split'
  echo '---------------'
  python aligned_corpus/split_DB.py $dir 1 | grep -oh '[0-9][0-9]*' > sym_count
fi

sed -n 1p sym_count > sms_sym
sed -n 2p sym_count > en_sym
rm sym_count

# train
echo '-----'
echo 'Train'
echo '-----'
python aligned_corpus/train.py $dir $model_dir sms_sym en_sym
rm sms_sym
rm en_sym
# evaluate
echo '--------'
echo 'Evaluate'
echo '--------'
python aligned_corpus/evaluate.py $dir $model_dir $results_dir
