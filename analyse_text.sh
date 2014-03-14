# -------------------------------------------------------------------------------------------------------
# ----------- ANALYSE TEXT ------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
# run script for text analysation
# desamb output is buffered per sentence
set_output="$(mktemp)"
gvf_output="$(mktemp)"
buffer="$(mktemp)"

#valency_file="/nlp/projekty/sysel/bin/valencyMap/data/verbalex.uni"
valency_file="/home/xstyrak/utils/get-valency-frames/frames/verbalex-content-analyser.txt"

# grammatic analysis
/home/xstyrak/utils/desamb/process_text.sh $1 |\

# preprocessing before set
/home/xstyrak/utils/get-valency-frames/syntactic_preprocessor.py |\
#/home/xstyrak/utils/desamb/replace_recommendations.py |\

while read token ; do
    echo $token >> $buffer
    if [ "$token" == "</s>" ]; then
        cat $buffer |\
        /nlp/projekty/set/set/set.py --marx 2>/dev/null |\
        sed 's/(k5.*)/()/g' > $set_output
        java -cp /nlp/projekty/sysel/bin/valencyMap/dist/ValencyMapper.jar valencymapper.ParseCorpora "$valency_file" $set_output > $gvf_output
        /home/xstyrak/utils/get-valency-frames/analyse_text.py $set_output $gvf_output
        #cat $set_output
	echo "" > $buffer
    fi
done
