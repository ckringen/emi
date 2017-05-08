$d = $1
$source = $2
$destination = $3

time xzcat $source | python count_skipgrams.py $d | gzip > $destination
