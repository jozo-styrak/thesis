#!/bin/sh
# arguments: input_dir filter_word
FILES="$(ls $1)"

for f in $FILES
do
#        python /home/xstyrak/thesis/grep_file.py "$1"/"$f" "$2"
    python ./pipeline_scripts/grep_file.py "$1"/"$f" "$2"
done

