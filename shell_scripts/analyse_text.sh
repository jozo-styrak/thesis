#!/bin/sh
set_output="$(mktemp)"

/home/xstyrak/thesis/shell_scripts/process_text.sh $1 |\
/home/xstyrak/thesis/ner_script.py |\
/home/xstyrak/thesis/shell_scripts/set.sh > $set_output
/home/xstyrak/thesis/analyse_text.py $set_output