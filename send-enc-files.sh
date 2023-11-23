#!/bin/bash

set -e -u
#set -x # Enable for debugging

recipient="put_the_recipient_name_or_email_here" # Or maybe pass it from command line?

all_enc_files=()

for file in "$@"
do
    if [[ -f $file ]]; then
        enc_filename=$(basename "$file.gpg")
        all_enc_files+=("$enc_filename")
        gpg --output "$enc_filename" --recipient $recipient --sign --encrypt "$file"
    else
        echo "'$file' is not a file, skipping..."
    fi
done

if [[ "${#all_enc_files[@]}" -ge 1 ]]; then
    echo "Sending the following files: ${all_enc_files[*]}"

    set +e +u # Delete encrypted files even if sending fails

    /full/path/to/sender/venv/bin/python /full/path/to/sender/sender.py "${all_enc_files[@]}"

    for enc_file in "${all_enc_files[@]}"
    do
        rm -v "$enc_file"
    done
else
    echo "No files were encrypted, quitting."
fi
