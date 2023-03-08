#!/bin/bash

# get the list of directories in the current directory
directories=( $(ls -d */) )

# loop through each directory in the directories array
for directory in "${directories[@]}"; do
  # move into the directory
  cd "$directory"
  cp ../{go.sh,mylammps.sh,in.react} ./
  
  item=$(echo "$directory" | sed 's/\///g') 
  echo "$directory"
  sed -i -e  "s/#####/${item}/g" go.sh
  llsubmit go.sh

  cd ../
done
