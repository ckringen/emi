#!/usr/bin/bash

python2 dep_search/query.py '_ <prt (VB|VBD|VBG|VBN|VBP|VBZ)' -m 0 -d '/om/user/futrell/en00aa.data/*.db' |
    python2 querypairs.py |
    python2 lemmatize_verbs.py |
    sh filter_v.sh > ../output/vp_pairs.tsv

cat ../output/vp_pairs.tsv |
    awk -F"\t" '{print $1 "\t" $2;}' | 
    sed "s/$/\t/g" |
    sh filter_vp.sh > ../output/vp_pairs_fullyrestricted.tsv

cat ../output/vp_pairs_fullyrestricted.tsv |
    python3 pmi_from_lines.py > ../output/vp_pmi_fullyrestricted.tsv

python2 dep_search/query.py '(VB|VBD|VBG|VBN|VBP|VBZ) >prt _' -m 0 -d '/om/user/futrell/en00aa.data/*.db' |
    python2 querypairs.py |
    awk -F"\t" '{print $2;}' |     
    python2 lemmatize_verbs.py |
    sed "s/$/\t0/g" |
    sh filter_v.sh |
    cat - ../output/vp_pairs.tsv |
    python3 pmi_from_lines.py |
    sh filter_vp.sh > ../output/vp_pmi_fullyrestricted_incnull.tsv
