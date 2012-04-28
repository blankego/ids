#! /usr/bin/env bash
BUILDDIR='impalpable_build'
if [ ! -e $BUILDDIR ]; then
   mkdir $BUILDDIR
fi
IME=impalpable
TWIST=TWIST
#generate scim-formatted table of glyphs
#echo 'generate glyph scim-table'
#python gen_glyph_scimtable.py glyphs.txt > $BUILDDIR/coded_glyphs.txt

#generate abbreviations
echo 'generate abbreviations'
python gen_abbr.py 

#generate code table of phrases
echo 'generate phrases code'
python gen_phrase_code.py phrases.txt > $BUILDDIR/coded_phrases.txt

#merge source parts to the full code table
echo 'merge code parts to one table'
cat  shorthands1.txt tra_abbr.txt  fullcodes.txt tra_plus.txt \
   $BUILDDIR/coded_phrases.txt >$BUILDDIR/table.txt
#generate frequency
echo 'generate frequency'
python add_frequency.py $BUILDDIR/table.txt > $BUILDDIR/table_with_freq.txt

#build scim table (add the header & footer to the code table)
echo 'create scim table'
if [[ $TWIST ]]; then
#swap 'z' and 'h' to mitigate the burden of left pinky
echo 'swap z h'
cat $BUILDDIR/table_with_freq.txt | tr 'zh' 'hz' \
   > $BUILDDIR/table_rearranged.txt
cat ${IME}_header.txt symbols.txt $BUILDDIR/table_rearranged.txt \
   > $BUILDDIR/$IME.in
else
cat freeime_header.txt symbols.txt $BUILDDIR/table_with_freq.txt \
   > $BUILDDIR/$IME.in
fi 
echo 'END_TABLE' >> $BUILDDIR/${IME}.in

#compile the scim table into binary file
echo 'compile scim table'
scim-make-table $BUILDDIR/$IME.in -b -o $BUILDDIR/$IME.bin

#install the ime
echo 'installing...'
sudo cp $BUILDDIR/$IME.bin /usr/share/scim/tables
pkill scim
scim -d

echo 'done!'
