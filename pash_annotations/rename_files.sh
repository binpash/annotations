#!/bin/bash

directory="/home/castlehoney/repos/research/annotations/pash_annotations/annotation_generation/annotation_generators"

for filename in $directory/*; do
    if [ -f "$filename" ]; then
        # Get the file name without the path
        base=$(basename "$filename")

        # Convert camelCase to snake_case
        snake_case=$(echo "$base" | sed 's/\([a-z]\)\([A-Z]\)/\1_\2/g' | tr '[:upper:]' '[:lower:]')

        # Construct the new file path
        new_path="$directory/$snake_case"

        # Rename the file
        mv "$filename" "$new_path"

        echo "Renamed: $base -> $snake_case"
    fi
done

