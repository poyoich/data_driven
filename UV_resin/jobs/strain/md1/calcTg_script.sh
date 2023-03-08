#!/bin/sh

directories=( $(ls -d */) )

rm tg.txt
for item in "${directories[@]}"; do
	echo "${item}"
	cd ${item}
    output=$(calc_Tg_CTE.py temp_vs_density.txt) 
    item=$(echo "$item" | sed 's/\///g') 
	cd ..
    echo "${item},${output}" >> ./tg.txt
done

