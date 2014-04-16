#!/bin/sh
# arguments: input_dir filter_word
FILES="$(ls $1)"

for f in $FILES
do
        python /home/xstyrak/thesis/filter_test.py "$1"/"$f" "$2"
done

