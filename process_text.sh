# processing script
# uses unitok to tokenize text
# added preprocessing and postprocessing of tagged output

# tokenization
cat $1 |\
/home/xstyrak/utils/unitok.py -n  |\
iconv -f utf-8 -t iso-8859-2 -c |\
/home/xstyrak/utils/desamb/add_s_tags.py |\
/home/xstyrak/utils/desamb/preprocess.py |\

/nlp/projekty/ajka/bin/ajka -n -c - |\
perl -pe '
	BEGIN { $m = shift(@ARGV) || "" }
	# ajka kouskuje pøíli¹ dlouhé øádky po 254 znacích, tak to musíme
	# napravovat (vadí to u pøíli¹ dlouhých znaèek, zejména <doc ...>)
	s/^(.{254}) \n$/$1/;

	if ($m eq "q" || $m eq "w") {
		# vyhození lemmat, které Marx nechce (malý jako k1)
		s/ <c>\S+qM//g;
		s/ <l>[^<\s]+(?= <l>|$)//g;
		}
	else {
		# nebo vyhození qM, èím¾ jsou tato lemmata signalizována
		s/<c>\S+\KqM//g;
		}' $2 |\
perl -pe 's/^(\d+)( ?)$/$1 <l>#num# <c>k4$2/' |\
/nlp/projekty/rule_ind/stat/remove.mSmDwH.pl |\
/nlp/projekty/rule_ind/stat/guesser.pl /nlp/projekty/rule_ind/stat/guesser.data $2 |\
perl -pe '
	# Znaèky nechceme upravovat (mohou mít v uvozovkách libovolný text
	# --- a pøihodilo se, ¾e nìco z následujícího zahoøelo ;-)
	next if /^</; 
	1 while s/(?:;\S+\K|;)q.//g;
	1 while s/>(který|jen¾ (?:(?!<l>).)+)y(.)/>$1x$2/;
	1 while s/^ne.*<l>být (?:(?!<l>).)+\KeA/eN/; # "chyba" (známá, principiální a "neopravitelná") v ajce
	s/>se <c>k3c4;xPyF/>sebe <c>k3xPyFc4/;
	s/>si <c>k3c3;xPyF/>sebe <c>k3xPyFc3/;
	s/k3([^;\s]*);(?:h.)?(x.y.|x.|y.)/k3$2$1/g;
	s/k4([^;\s]*);(?:h.)?(x.y.|x.|y.)/k4$2$1/g;
	s/k5(.*);[^\s]+/k5$1/g;
	s/nD/nP/g;

	s/ <c>[^<]+;wZ[^\s]*//g;
	s/k8;x(\w)/k8x$1/g;

	s/ <c>\S+\K;\S+//g;
	s/ <c>[^<]+;?wH//g;
	s/ <l>[^<\s]+(?= <l>|$)//g;
	s/ +$//;
	' |\
/nlp/projekty/rule_ind/stat/remove.pl /nlp/projekty/rule_ind/stat/remove.znacky |\
/nlp/projekty/rule_ind/stat/remove.c1.pl |\
/nlp/projekty/rule_ind/stat/remove.rules.pl |\
/nlp/projekty/rule_ind/stat/filtr_input.perl |\
/nlp/projekty/rule_ind/stat/disna d |\
/nlp/projekty/rule_ind/stat/filtr_output_val.perl |\
perl -pe 's/\(\\\)/\\/' |\
perl -pe '
	next if /^</;
	# Správnì by to nemìlo být zakomentované, ale Ale¹ chtìl k3xD atp.
	# Tak¾e teï vracené znaèky neodpovídají ajce, co¾ asi není pøíli¹ problém.
	# 1 while s/k3[yx]./k3/g;
	s/>sebe <c>k3c3/>si <c>k3c3/;
	s/>sebe <c>k3c4/>se <c>k3c4/;
	s/k5([^\s])t./k5$1/g;
	s/k5([^\s]*)p([^\d])/k5${1}g$2/g;
	' |\
perl -ne 'BEGIN { $/ = "</s>\n" } # odstranìní hacku v tecky.pl
	$old =~ s~<g />\n\.\n$/~~ if s~<s hack="1">\n~~;
	print $old if $old;
	$old = $_;
	END { print $old }
	' |\
/nlp/projekty/rule_ind/stat/hack.pl $2 |\
/nlp/projekty/rule_ind/stat/statdesam.pl $2 |\
perl -pe 's/<[^\t]+>\K\t.*//' |\

# output postprocessing
iconv -f iso-8859-2 -t utf-8 2>/dev/null |\
/home/xstyrak/utils/desamb/postprocess.py /home/xstyrak/utils/desamb/data/replacement.utf8.data
#/home/xstyrak/utils/desamb/connect_abbrs.py