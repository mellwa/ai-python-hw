#!/usr/bin/env bash

mkdir -p input_dir
mkdir -p output_dir
mkdir -p sample_output

INPUT_FILES=./input_dir/input*.txt
#for f in ${INPUT_FILES}
total_num=`ls -l ./input_dir/ | wc -l`
((total_num--))
echo "total ${total_num} tests"
for f in ./input_dir/input{1..7}.txt
do
    cp ${f} ./input.txt
    time python hw3cs561s2018.py
    echo ${f}
    input_file_name=$(basename "$f")
    num="${input_file_name##*ut}"
    num="${num%.*}"
    if [  -e ./output.txt ]
    then
        mv ./output.txt ./output_dir/output"${num}".txt
    fi
    echo "finished ${num}/${total_num}"
done
rm ./input.txt