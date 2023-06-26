#!/bin/bash
LOGIN_USERNAME=root
ACCOUNT_USERNAME=tom
# IPS=$(doctl compute droplet list --format "PublicIPv4")

# SERVER_ARRAY=($(echo $IPS | cut -d' ' -f 3-50))
chemical=""
server=""
version=""
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --chemical)
            chemical="$2"
            shift
            ;;
        --server)
            server="$2"
            shift
            ;;
        --version)
            version="$2"
            shift
            ;;
        *)
            # Invalid flag
            echo "Invalid flag: $key"
            exit 1
            ;;
    esac
    shift
done

echo ${server}
echo ${chemical}
echo ${version}

MODEL_OUTPUT_DIR=data_input/MSSC_DVC/output/saved_model/saved_models/${chemical}/std
FILE_PATTERN="model.hdf5"

LOCAL_DIR=/home/tom/DSML125/QC_Model_Predictions/dl_models_all_chems_20210414/${version}/${chemical}

mkdir --parents ${LOCAL_DIR}



# [ -z "${ACCOUNT_USERNAME}" ] && { echo "The unix account username must be set!"; exit; }
# [ -z "${MODEL_OUTPUT_DIR}" ] && { echo "The model output directory must be set!"; exit; }
# [ -z "${FILE_PATTERN}" ] && { echo "The file pattern must be set!"; exit; }

if ! type inotifywait &>/dev/null
then
#  echo "You are missing the inotifywait dependency. Install the package inotify-tools (apt install inotify-tools)"
#  exit 1
  sudo apt install inotify-tools
fi



ssh -o GlobalKnownHostsFile=/dev/null -o UserKnownHostsFile=/dev/null -o "StrictHostKeyChecking no" "${LOGIN_USERNAME}@${server}" "if [ -d '/home/${ACCOUNT_USERNAME}/${MODEL_OUTPUT_DIR}' ]; then exit 0; else exit 1; fi" >/dev/null 2>&1

sleep 300

if [ $? -eq 0 ] 
then
  scp -r ${LOGIN_USERNAME}@${server}:/home/${ACCOUNT_USERNAME}/${MODEL_OUTPUT_DIR} ${LOCAL_DIR}
else
  ( ssh -o GlobalKnownHostsFile=/dev/null -o UserKnownHostsFile=/dev/null -o "StrictHostKeyChecking no" ${LOGIN_USERNAME}@${server} inotifywait -e close_write,moved_to,create -m /home/${ACCOUNT_USERNAME}/${MODEL_OUTPUT_DIR} |
    while read -r directory events filename; do
      echo ${server} ${directory} ${events} ${filename}
      if [[ ${filename} =~ ${FILE_PATTERN} ]]
      then
        if [[ ${events} =~ "CLOSE_WRITE" ]]
        then
        filename=$(printf '%q' "$filename")
        echo "Detected: " ${server} ${directory} ${events} ${filename}
        scp -r ${LOGIN_USERNAME}@${server}:/home/${ACCOUNT_USERNAME}/${MODEL_OUTPUT_DIR} ${LOCAL_DIR}/${chemical}
        wait
        break
        fi
      fi
    done 
  )
  fi

