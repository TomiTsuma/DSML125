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
  - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDJwILqw2pWl77Mn4ciC+J2ZFLGtE6PIx4AhkdrxZMnIGJpqeqJRsb2gNl8IDyiKpFpT9gnJZT4e3NtZ49Fjtk3haqu56tjW0M8CT5IMajJRAyj/298pQPiwWHs1gQ4cJCJa3aDWpqPeg/YqY/EOXZXj8EuVbFjSaHe3caeNaXRRQMZQS0N+NmFBu4HgzUnoKujfrzFapVClhk7tdZv9xcwfDubMtvObmn8upfuYw9SxQanNmgK3YyoHjji3BPIF86JAX+BZeyPjekcEpT/zTEDuMbitItrpEJyU7jsb6fhjGhzF8RXiq5hGZPGntVkq39zdIVLE6dt6eMnFuvPZ6t1V0o4HS6O0vcfCaOQi/ewdRmqOdifrqZRjgH7JXkhHyS+VUxmZ+h87yn0cbcyFeWuAq+teupjJCR5fxlOlm7ZSB8FYLyYDdYIEWq0XuK2GoYc7F3W+LVkWnjlM/ynjKHIEpovkwAd7ocIyaUD1Jfq4Irnh9zgZirAYYNiVpjr9Os= tom@model-dev-s-4vcpu-8gb-ams3-01
  - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCmxcBpzsg94lykmDNZqsFhagxv093kgXPZh86F/FskTy6IR0YNlnMJ2IV79A1TfLFef5P4V1PFGaXUErgKBn3Gry7lHM7gjcvjgkiurk/8Pzhr7qCzTff1V0L9EhJzC+h5Ka6dK8X9ob9N7CEP4/C+sI0SfmtmKJqUben1VeiA1Ru6fVd/DGGKVPVx6nyM0unGqICSi1fs7hlgd4KxPK0BFZ6UJaG8AnyeNDDt4XasS3D5103BUakrU5w6rjnyYKziUul62Og6FMlzXAo6eA/776trUtpB8na8emxniomvQs4pX9hfHeHFtq3SHuIwLbdfjMnLK7ce0iFZsePt137kET+CN55jxNXVCsjiCCj+HncPjCHxXsLcas4IEJS9iMxu3G46WTpezz1Vc4g+ijMXkPyQRkmS4q9EfuLLaEWinwEi+1GuvkGxrcKVFuvnRnPmvIidI98lGPYf5cO+JsEUNH9Uy5dvD1YlbO91EM6ev3NVas7hd+te0e8j4yLS8Z0= tommy@DESKTOP-MN2KUGJ
runcmd:
  - tmux
  - cd /home/${DO_USERNAME}/.ssh
  - echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCmxcBpzsg94lykmDNZqsFhagxv093kgXPZh86F/FskTy6IR0YNlnMJ2IV79A1TfLFef5P4V1PFGaXUErgKBn3Gry7lHM7gjcvjgkiurk/8Pzhr7qCzTff1V0L9EhJzC+h5Ka6dK8X9ob9N7CEP4/C+sI0SfmtmKJqUben1VeiA1Ru6fVd/DGGKVPVx6nyM0unGqICSi1fs7hlgd4KxPK0BFZ6UJaG8AnyeNDDt4XasS3D5103BUakrU5w6rjnyYKziUul62Og6FMlzXAo6eA/776trUtpB8na8emxniomvQs4pX9hfHeHFtq3SHuIwLbdfjMnLK7ce0iFZsePt137kET+CN55jxNXVCsjiCCj+HncPjCHxXsLcas4IEJS9iMxu3G46WTpezz1Vc4g+ijMXkPyQRkmS4q9EfuLLaEWinwEi+1GuvkGxrcKVFuvnRnPmvIidI98lGPYf5cO+JsEUNH9Uy5dvD1YlbO91EM6ev3NVas7hd+te0e8j4yLS8Z0= tommy@DESKTOP-MN2KUGJ" >> authorized_keys
  - echo "
  - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDJwILqw2pWl77Mn4ciC+J2ZFLGtE6PIx4AhkdrxZMnIGJpqeqJRsb2gNl8IDyiKpFpT9gnJZT4e3NtZ49Fjtk3haqu56tjW0M8CT5IMajJRAyj/298pQPiwWHs1gQ4cJCJa3aDWpqPeg/YqY/EOXZXj8EuVbFjSaHe3caeNaXRRQMZQS0N+NmFBu4HgzUnoKujfrzFapVClhk7tdZv9xcwfDubMtvObmn8upfuYw9SxQanNmgK3YyoHjji3BPIF86JAX+BZeyPjekcEpT/zTEDuMbitItrpEJyU7jsb6fhjGhzF8RXiq5hGZPGntVkq39zdIVLE6dt6eMnFuvPZ6t1V0o4HS6O0vcfCaOQi/ewdRmqOdifrqZRjgH7JXkhHyS+VUxmZ+h87yn0cbcyFeWuAq+teupjJCR5fxlOlm7ZSB8FYLyYDdYIEWq0XuK2GoYc7F3W+LVkWnjlM/ynjKHIEpovkwAd7ocIyaUD1Jfq4Irnh9zgZirAYYNiVpjr9Os= tom@model-dev-s-4vcpu-8gb-ams3-01" >> authorized_keys
  - cd /home/${DO_USERNAME}
  - git config --global user.name "${DO_GITHUB_USERNAME}"
  - git config --global user.email "${DO_GITHUB_EMAIL}"
  - git clone https://${DO_GITHUB_TOKEN}@github.com/${DO_GITHUB_USERNAME}/DSML125.git DSML125
  - wait
  - cd DSML125
  - export AWS_ACCESS_KEY_ID=${DO_AWS_ACCESS_KEY_ID}
  - export AWS_SECRET_ACCESS_KEY=${DO_AWS_ACCESS_KEY}
  - export USERNAME=${DO_USERNAME}
  - sudo bash odbc_install.sh
  - bash repos.sh
  - mkdir DSML87/inputFiles
  - mkdir outputFiles
  - sudo bash r_installation.sh
  - sudo bash vpn_con.sh
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

ssh root@${IP} << 'EOF'
while :
do
    if cd /home/tom/DSML125/inputFiles &> /dev/null 
    then
        break
    else
        echo "DSML125 not created yet"
        sleep 10
    fi
done
EOF
wait

scp -r /home/tom/DSML125/inputFiles root@${IP}:/home/tom/DSML125
wait
ssh root@${IP} << 'EOF'

while :
do
    if python3 -c "import notebook";
    then
        echo "notebook is installed."
        python3 /home/tom/DSML125/cli.py -m /home/tom/DSML125/inputFiles/modeling-instructions.csv -p /home/tom/DSML125/inputFiles/phone_numbers.csv -e /home/tom/DSML125/inputFiles/model_evaluation.csv -v v2.4
        break
    else
        echo "notebook is not installed."
    fi
    sleep 5
done
EOF

wait

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

scp -r root@${IP}:/home/tom/DSML125/outputFiles /home/tom/DSML125/outputFiles






