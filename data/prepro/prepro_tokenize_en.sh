#!/bin/bash
LANGCODE=en
SCRIPTS=scripts
TCMODEL=truecasemodels/truecase-model.en
scripts/normalize-punctuation.perl $LANGCODE | \
scripts/tokenizer.perl -a -l $LANGCODE | \
scripts/truecase.perl -model ${TCMODEL}
