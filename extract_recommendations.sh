#!/bin/sh
set_output="$(mktemp)"

#/home/xstyrak/thesis/pipeline_scripts/tag_file.sh $1 |\
#/home/xstyrak/thesis/ner_script.py |\
#/home/xstyrak/thesis/pipeline_scripts/set.sh > $set_output
#/home/xstyrak/thesis/extract_recommendations.py $set_output

./tag_file.sh $1 |\
./pipeline_scripts/ner_script.py |\
./set.sh > $set_output
./extract_recommendations.py $set_output