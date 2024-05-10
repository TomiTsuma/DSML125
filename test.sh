#!/bin/bash

ssh root@68.183.7.73 << 'EOF'

while :
do
    if python3 -c "from pypdf import PdfReader" &> /dev/null
    then
        echo "pypdf is installed."
        break
    else
        echo "pypdf is not installed."
    fi

    # Wait for some time before checking again (e.g., every 5 seconds)
    sleep 5
done
EOF

