#!/bin/bash

rm -r output_dir error_dir
mkdir -p inputs
mkdir -p output_dir
mkdir -p error_dir

INPUT_FILES=./inputs/input*.txt
#for f in ${INPUT_FILES}
total=`ls -l ./inputs/ | wc -l`
((total--))
echo 'total '${total}' tests'
finished=0
for f in ./inputs/input*
do
    cp ${f} ./input.txt
    echo '-----------------------'
    time python hw2cs561s2018.py
    echo 'testing' ${f}
    input_file_name=$(basename "$f")
    num="${input_file_name##*ut}"
    num="${num%.*}"
    if [ -e ./output.txt ]
    then
        python test.py
        mv ./output.txt ./output_dir/output"${num}".txt
    fi
    if [ -e ./error.txt ]
    then
        mv ./error.txt ./error_dir/error"${num}".txt
    fi
    ((finished++))
    echo "finished ${finished}/"${total}
    echo '-----------------------'
done
rm ./input.txt
