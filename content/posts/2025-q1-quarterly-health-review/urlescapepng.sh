#!/bin/bash

for file in "$1"/*.png; do [ -e "$file" ] || continue; mv "$file" "$(dirname "$file")/$(basename "$file" | tr ' ' '_' | tr -d '"&?<>#%{}|\\^~[]`")"; done
echo "Renaming complete."

