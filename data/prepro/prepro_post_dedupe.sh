#!/bin/bash
# only parameter: $1 language
LANGCODE=$1
SCRIPTDIR=`dirname $0`/scripts
iconv -c --from UTF-8 --to UTF-8 | \
$SCRIPTDIR/sanitize_unicode.py | \
$SCRIPTDIR/strip_markup.perl | \
$SCRIPTDIR/remove_email.perl | \
$SCRIPTDIR/remove_whitespace.perl | \
$SCRIPTDIR/normalize-punctuation.perl $LANGCODE | \
$SCRIPTDIR/split-sentences.perl -l $LANGCODE -splitlinebreak 
