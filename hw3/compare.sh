#!/usr/bin/env bash

if [ -e ./diff_result.txt ]
then
    rm ./diff_result.txt
fi

OUTPUT_FILES=./output_dir/*
SAMPLE_OUTPUT_FILES=./sample_output/*

total=0
sample_array=()
output_array=()
for file in ${SAMPLE_OUTPUT_FILES}
do
    sample_array+=(${file})
    ((total+=1))
done

for file in ${OUTPUT_FILES}
do
    output_array+=(${file})
done

result_array=()
diff_files_num=0
for ((i=0; i<total;i++))
do
    file_name="${output_array[i]##*/}"
    if cmp -s -- ${sample_array[i]} ${output_array[i]}; then
        echo "${file_name} is same"
    else
        echo "${file_name} is different"
        result_array+=("${file_name} is different")
        ((diff_files_num++))
    fi
done

echo "total ${total} output files and ${diff_files_num} files are different with sample output files"

for i in "${result_array[@]}"
do
    echo $i >> diff_result.txt
done
