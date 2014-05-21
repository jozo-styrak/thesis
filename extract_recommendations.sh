#!/bin/sh
# main running script
# input from file or from pipe
# args: -f filename -s -o
# if -f is not specified, input is read from pipe
# -s prints out sentences with tagged entities
# -o output non-json format also

file_specified=0
s_out=""
o_out=""
filestream="-"
error=0

# read command line arguments
for i in "$@"
do

if [ "$file_specified" -gt 0 ]; then
    filestream="$i"
    file_specified=0
elif [ "$i" = "-f" ]; then
    file_specified=1
elif [ "$i" = "-s" ]; then
    s_out="-s"
elif [ "$i" = "-o" ]; then
    o_out="-o"
else
    error=1
fi

done

if [ $error -gt 0 ]; then

echo "Error reading command line arguments"

else

# the main code
#set_output="$(mktemp)"

cat $filestream |\
./tag_stream.sh |\
./ner_script.py |\
./set.sh |\
./extract_recommendations.py "$s_out" "$o_out"

fi