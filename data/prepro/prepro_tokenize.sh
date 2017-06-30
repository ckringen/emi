#!/bin/bash
# only parameter: $1 language

if [ $# -ne 2 ]
then
  echo "Usage: `basename $0` {language} {truecase_model}"
  exit -1
fi

LANGCODE=$1
TCMODEL=$2
SCRIPTDIR=scripts

iconv -c --from UTF-8 --to UTF-8 | \
${SCRIPTDIR}/unescape_html.perl | \
${SCRIPTDIR}/normalize-punctuation.perl $LANGCODE | \
${SCRIPTDIR}/remove_whitespace.perl | \
${SCRIPTDIR}/tokenizer.perl -a -l $LANGCODE | \
${SCRIPTDIR}/truecase.perl -model $TCMODEL
