#!/bin/bash


DO_USERNAME=tom
DO_GITHUB_USERNAME=TomiTsuma
DO_GITHUB_TOKEN=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
DO_GITHUB_EMAIL=tommytsuma7@gmail.com

DO_TOKEN=dop_v1_99662bc2fc3e366d47a5719377dea0c3528885826e561a611466ec15efe0a5bd
DO_AWS_ACCESS_KEY_ID=DO00JVCF7VU9NR8R9KUC
DO_AWS_ACCESS_KEY=qw7fwzXbo90pYNVgybQbodide616IklbcR21y6G8EOI
DO_SLACK_API_TOKEN=xoxb-589741945461-590957910966-krg84CEBEiUlzb7D6uHGJcw3
DO_SSH_KEY=70:8d:65:a6:4b:f9:0b:cd:9e:25:38:78:62:27:e0:d4
#Not required for Wandb
# DO_WANDB_KEY=$DO_WANDB_KEY

SPC_PATH=/home/tom/data_input/MSSC_DVC/spc/spc.csv
WET_PATH=/home/tom/data_input/MSSC_DVC/wetchem/wetchem.csv
SPLITS_DIR=/home/tom/data_input/MSSC_DVC/splits
BASE_DIR=/home/tom/data_input/MSSC_DVC

[ -z "${DO_USERNAME}" ] && { echo "The unix account username must be set!"; exit; }
[ -z "${DO_TOKEN}" ] && { echo "The DigitalOcean access token must be set!"; exit; }
[ -z "${DO_AWS_ACCESS_KEY_ID}" ] && { echo "The AWS access key ID must be set!"; exit; }
[ -z "${DO_AWS_ACCESS_KEY}" ] && { echo "The AWS access key must be set!"; exit; }
[ -z "${DO_SLACK_API_TOKEN}" ] && { echo "The Slack API token must be set!"; }
[ -z "${DO_SSH_KEY}" ] && { echo "The SSH key must be set!"; exit; }


chem=$@


tag=$chem
if [[ ${chem} =~ 'ec_(salts)' ]]
    then
      tag='ec'
fi
doctl compute tag create trainer-dl4-${tag}


# DO_MODEL_OUTPUT_DIR=output/saved_model_${chem}
DO_MODEL_OUTPUT_DIR=output/saved_model

DO_COMMIT_MSG="Add model for ${chem} using MSSC version ${DO_MSSC_RELEASE_VERSION}"

DO_USER_DATA=$(cat <<-_EOF_
#cloud-config
users:
    - name: ${DO_USERNAME}
      groups: sudo
      shell: /bin/sh
      sudo: ['ALL=(ALL) NOPASSWD:ALL']
package_upgrade: true
packages: 
  - inotify-tools
  - git
  - build-essential
  - htop
ssh_authorized_keys:
  - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCmcWRRIVE5fVz9BUnVeLlWxIY9vzwCzoSnoqHuJ/WeFtsogFOG9iq7Js2HbHKwwVs4KXYtsIWws1Y1/Jx8798P6LBC/Ky25mQqqCOlR6nDAZ2BzDh+V5og7zyEDkaVan46gdSlwFJ4ZOgmMIRa56wZNsAiJd7r5NfAsLZxj98sLXGrp5P/aTZqthHEV1ZdWiM0FROWsMlCvYPGjX6TWw02b0VPejMgTj7wt40venPyrZXxV4SQ/2OJg9PbJAbOTF1m17fgqYSbQQRmy4PPM/SS4ZZTfh9SMPHmYCYm9Yp7UH3sX6WKv9YEeIfW1rdjUG5YIrIrivQuoVbpK03x1aViLUvX8pgONYmBp/PZNm4w+IahFu68AUmxmGs1Mhh4bYlk9wNMW5L96NmshsUEsvL5AwqvqUHUdqKxigxPkeTQ1VcaK+gyfqa21RwQTM7xn+USJnvn0rAla4wjrDEG8SLejd70wGDLvcQ6HbUhdGYTjsMdhkUj7TLf2S8Lg5LEwUU  tom@model-dev-s-4vcpu-8gb-ams3-01
  - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCmcWRRIVE5fVz9BUnVeLlWxIY9vzwCzoSnoqHuJ/WeFtsogFOG9iq7Js2HbHKwwVs4KXYtsIWws1Y1/Jx8798P6LBC/Ky25mQqqCOlR6nDAZ2BzDh+V5og7zyEDkaVan46gdSlwFJ4ZOgmMIRa56wZNsAiJd7r5NfAsLZxj98sLXGrp5P/aTZqthHEV1ZdWiM0FROWsMlCvYPGjX6TWw02b0VPejMgTj7wt40venPyrZXxV4SQ/2OJg9PbJAbOTF1m17fgqYSbQQRmy4PPM/SS4ZZTfh9SMPHmYCYm9Yp7UH3sX6WKv9YEeIfW1rdjUG5YIrIrivQuoVbpK03x1aViLUvX8pgONYmBp/PZNm4w+IahFu68AUmxmGs1Mhh4bYlk9wNMW5L96NmshsUEsvL5AwqvqUHUdqKxigxPkeTQ1VcaK+gyfqa21RwQTM7xn+USJnvn0rAla4wjrDEG8SLejd70wGDLvcQ6HbUhdGYTjsMdhkUj7TLf2S8Lg5LEwUU= tom@model-dev-s-4vcpu-8gb-ams3-01
  - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCfji6Oqm12zeZ8yhsoX7wNmY/S9JdVXhTKu7kRhLWJbtRAV7sUYa5GjmAg//37CYC6xIYBgG6/YA3e69UwnhqeFvNl83LZTM6jSQXNg75626URfc0+WetnPhk+nX3Z4F21yVh0tji3v5rzbPR6v1s0LGevRWpNMBqH0EmiPojhpI6VgyrUsn2OkMy2mhTjyJ6jz6I7j6b4YsOWJdZ70dNbD4r7UbuIrhRRvCvi9nYv/g622nmE24VNzTYzUBYFM+3F4syrFoE8unr+L9f4ZoVw9XaUaOJK3v8G8BQ+O/pTbIKMkGWQ8Z5eU2oRlkJlYGk5/Bx5EFOeW5y82+FT1/lp root@trainer
  - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDPXZvFwJjFaIfKiU+Akpojv5tIXZO7WUZb9MY/mge+uxCFqRXd8Th1e2mgzVqoRVFUobvUvqOHuqu3KeR0PBscwbFekQsS460iowOLdZcxl3V23V4LqmQh+jiyLDN8S0QlZvLHMjPJxB1yGjZfLepQ8/NROk53jEw3RkumsmsKMXp5gU23IgnpcR3P6LQkWrutQaoU9sT1o8JPGrcOn0+TBp5oitKMGkaZnPCoFHJ/auWfF0QktC+oEYRD1WCTkJUCX07C7X3eYkyEmnCZcjAIW9vE3ljrK62yZwgXGtImiLHYvUOX1Y7SbHWXeNybGFTTxxf86bJkBxsWpgCMLj9HBetOCht6fTfsT5Ze1bdlowx7Y8JJSryLQUdoVRx5/TFn5F29HmyZV/v7K9+KW3TW3L7ouJx9YsWwUMJ9NZXfLpwPFp3hwwR40YMBK4Fko2CBXQrWIs2R0mVpm+o8ELfDudFFvp0EI5XhgmyDy1/ze9xrkjf6ongBsxoQ8r7kV4k= tsuma thomas@DESKTOP-A4FB8FQ
runcmd:
  - tmux
  - cd /home/${DO_USERNAME}/.ssh
  - echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDPXZvFwJjFaIfKiU+Akpojv5tIXZO7WUZb9MY/mge+uxCFqRXd8Th1e2mgzVqoRVFUobvUvqOHuqu3KeR0PBscwbFekQsS460iowOLdZcxl3V23V4LqmQh+jiyLDN8S0QlZvLHMjPJxB1yGjZfLepQ8/NROk53jEw3RkumsmsKMXp5gU23IgnpcR3P6LQkWrutQaoU9sT1o8JPGrcOn0+TBp5oitKMGkaZnPCoFHJ/auWfF0QktC+oEYRD1WCTkJUCX07C7X3eYkyEmnCZcjAIW9vE3ljrK62yZwgXGtImiLHYvUOX1Y7SbHWXeNybGFTTxxf86bJkBxsWpgCMLj9HBetOCht6fTfsT5Ze1bdlowx7Y8JJSryLQUdoVRx5/TFn5F29HmyZV/v7K9+KW3TW3L7ouJx9YsWwUMJ9NZXfLpwPFp3hwwR40YMBK4Fko2CBXQrWIs2R0mVpm+o8ELfDudFFvp0EI5XhgmyDy1/ze9xrkjf6ongBsxoQ8r7kV4k= tsuma thomas@DESKTOP-A4FB8FQ" >> authorized_keys
  - echo "
  - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCmcWRRIVE5fVz9BUnVeLlWxIY9vzwCzoSnoqHuJ/WeFtsogFOG9iq7Js2HbHKwwVs4KXYtsIWws1Y1/Jx8798P6LBC/Ky25mQqqCOlR6nDAZ2BzDh+V5og7zyEDkaVan46gdSlwFJ4ZOgmMIRa56wZNsAiJd7r5NfAsLZxj98sLXGrp5P/aTZqthHEV1ZdWiM0FROWsMlCvYPGjX6TWw02b0VPejMgTj7wt40venPyrZXxV4SQ/2OJg9PbJAbOTF1m17fgqYSbQQRmy4PPM/SS4ZZTfh9SMPHmYCYm9Yp7UH3sX6WKv9YEeIfW1rdjUG5YIrIrivQuoVbpK03x1aViLUvX8pgONYmBp/PZNm4w+IahFu68AUmxmGs1Mhh4bYlk9wNMW5L96NmshsUEsvL5AwqvqUHUdqKxigxPkeTQ1VcaK+gyfqa21RwQTM7xn+USJnvn0rAla4wjrDEG8SLejd70wGDLvcQ6HbUhdGYTjsMdhkUj7TLf2S8Lg5LEwUU= tom@model-dev-s-4vcpu-8gb-ams3-01" >> authorized_keys
  - cd /home/${DO_USERNAME}
  - git config --global user.name "${DO_GITHUB_USERNAME}"
  - git config --global user.email "${DO_GITHUB_EMAIL}"
  - git clone https://${DO_GITHUB_TOKEN}@github.com/${DO_GITHUB_USERNAME}/DSML125.git DSML125
  - cd DSML125
  - export AWS_ACCESS_KEY_ID=${DO_AWS_ACCESS_KEY_ID}
  - export AWS_SECRET_ACCESS_KEY=${DO_AWS_ACCESS_KEY}
  - export USERNAME=${DO_USERNAME}
  - sudo bash odbc_install.sh
  - bash repos.sh
  - mkdir DSML87/inputFiles
  - mkdir outputFiles
  - sudo bash r_installation.sh
  - wait
  - sudo apt-get install python3
  - sudo apt -yq install python3-pip
  - python3 -m pip install -r requirements.txt
_EOF_
)

echo "${DO_USER_DATA}" > /home/tom/DSML125/preparation.cloudinit


ID=$(doctl compute droplet create trainer-dl --region ams3 --image ubuntu-20-04-x64 --size s-4vcpu-8gb --ssh-keys $DO_SSH_KEY --user-data-file /home/tom/DSML125/preparation.cloudinit --tag-name trainer-dl4-${tag} --format "ID" --no-header)
echo ${ID}
sleep 300
IP=$(doctl compute droplet get $ID --format PublicIPv4 --no-header)
echo ${IP}

scp -r /home/tom/DSML125/inputFiles root@${IP}:/home/tom/DSML125

ssh root@${IP} << 'EOF'

while :
do
    if python3 -c "import notebook" &> /dev/null
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



ssh root@${IP} << 'EOF'
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

ssh root@${IP} "inotifywait -e create /home/tom/DSML125/outputFiles/final" | while read -r directory event file; 
do
        echo "File $file was created in $directory"
        scp -r root@${IP}:/home/tom/DSML125/outputFiles /home/tom/DSML125/outputFiles
        break
        # Add your custom logic here
done


