#!/bin/bash

# This Shell script compresses and archives the files that have been modified in the last 24 hours in a specified folder
# The script takes as arguments the folder that we want to archive and where we want to save the resulting compressed file

# This checks if the number of arguments is correct
# If the number of arguments is incorrect ( $# != 2) print error message and exit
if [[ $# != 2 ]]
then
  echo "backup.sh target_directory_name destination_directory_name"
  exit
fi

# This checks if argument 1 and argument 2 are valid directory paths
if [[ ! -d $1 ]] || [[ ! -d $2 ]]
then
  echo "Invalid directory path provided"
  exit
fi

# Set the command line arguments as variables
targetDirectory=$1
destinationDirectory=$2

# Display the command line arguments as variables
echo "The target directory is $targetDirectory"
echo "The destination directory is $destinationDirectory"

# To set a variable equal to the output of a command you can use command substitution: $() or ` `
# Get the current timestamp expressed in seconds
currentTS=`date +%s`

# Set the name of the compressed file that will be create
backupFileName="backup-$currentTS.tar.gz"

# We're going to:
  # 1: Go into the target directory
  # 2: Create the backup file
  # 3: Move the backup file to the destination directory

origAbsPath=`pwd`
cd $destinationDirectory
destDirAbsPath=`pwd`
cd $origAbsPath
cd $targetDirectory

# Math can be done using $(()); for example: zero=$((3 * 5 - 6 - 9))
# We need the files that have been updated in the last 24 hours
yesterdayTS=$(($currentTS - 24 * 60 * 60))

# This line declares an array. An array contains a list of values.
declare -a toBackup

for file in $(ls)
do
  # Check whether the $file was modified within the last 24 hours
  if ((`date -r $file +%s` > $yesterdayTS))
  then
    # Items can be appended to arrays using the syntax : myArray+=($myVariable)
    toBackup+=($file)
  fi
done

# Compress and archive the files
tar -czvf $backupFileName ${toBackup[@]}

# Copy the compressed file to the destination folder
cp $backupFileName $destDirAbsPath
