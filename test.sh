#!/bin/bash

ssh root@159.223.230.245 << 'EOF'

while :
do
    if python3 -c "python3 -m notebook" &> /dev/null
    then
        echo "notebook is installed."
        python3 cli.py -m /home/tom/DSML125/inputFiles/modeling-instructions.csv -p /home/tom/DSML125/inputFiles/phone_numbers.csv -e /home/tom/DSML125/inputFiles/model_evaluation.csv -v v2.4
        break
    else
        echo "notebook is not installed."
    fi
    sleep 5
done
EOF
