#!/bin/bash

# Function to recursively process directories
process_directory() {
    local directory="$1"
    for file in "$directory"/*; do
        if [ -e "$file" ]; then
            if [ -L "$file" ]; then
                # Check for symbolic links to avoid infinite loops
                link_target=$(readlink -f "$file")
                if [ "$link_target" == "$directory" ]; then
                    continue
                fi
            fi
            # Run `ls -Z` on the file
            ls_output=$(ls -Z "$file" 2>/dev/null)
            if [[ "$ls_output" =~ ^[^:]*:\? ]] || [[ "$ls_output" =~ :unlabeled ]]; then
                # Output the path if it matches the criteria
                echo "$file"
            fi
            if [ -d "$file" ]; then
                # If it's a directory, recursively process it
                process_directory "$file"
            fi
        fi
    done
}

# Start processing from the root directory
process_directory "/"


