#!/bin/bash
set -e
input=".env"
rm example.env -f
while read -r line
do
    IP=$(echo $line | tr "=" "\n")
    for i in $IP
    do
        echo "$i=\"\"" >> "example.env"
        break
    done
done < "$input"