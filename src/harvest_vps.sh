particles=`cat ../data/particles.regex`
grep -oe "\W.*/VB.*/.*/0 $particles/RB/advmod/1" | sed "s/\/.* / /g" | sed "s/\/.*$//g" | sed "s/\t//g" 
