#!/bin/bash

ssh root@68.183.7.73 << 'EOF'
while :
do
    if cd /home/tom/DSML125/outputFiles/final &> /dev/null 
    then
        break
    else
        echo "Not found"
        sleep 5
    fi
done
EOF

ssh root@68.183.7.73 "inotifywait -e create /home/tom/DSML125/outputFiles/final" | while read -r directory event file; 
do
        echo "File $file was created in $directory"
        scp -r root@68.183.7.73:/home/tom/DSML125/outputFiles /home/tom/DSML125/outputFiles
        break
        # Add your custom logic here
done

