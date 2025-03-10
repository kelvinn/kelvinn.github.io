#!/bin/bash
# Take a directory of .md files, and move each
# into it's own folder of the same name,
# then rename the file index.md
# md_to_page_bundle.sh in_dir out_dir
# Doesn't work with spaces in the folder names!

for f in $1/*.md;
do
    filename=$(basename -- "$f")
    postname="${filename%.*}"
    newdir="$2/$postname"
    mkdir "$newdir"
    cp "$f" "$newdir/index.md"
done
