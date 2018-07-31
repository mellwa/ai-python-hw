#!/bin/bash

mkdir -p input_dir
mkdir -p output_dir
mkdir -p sample_output

INPUT_FILES=./input_dir/input*.txt
#for f in ${INPUT_FILES}
num=`ls -l ./input_dir/ | wc -l`
((num--))
echo ${num}
for f in ./input_dir/input{1..1000}.txt
do
    cp ${f} ./input.txt
    python hw1cs561s2018.py
    echo ${f}
    input_file_name=$(basename "$f")
    num="${input_file_name##*ut}"
    num="${num%.*}"
    if [  -e ./output.txt ]
    then
        mv ./output.txt ./output_dir/output"${num}".txt
    fi
    echo "finished ${num}/1000"
done
rm ./input.txt
