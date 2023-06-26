#!/bin/bash

if ! command -v openvpn &> /dev/null; then
    sudo apt install openvpn
fi


sudo openvpn --config tsuma__ssl_vpn_config.ovpn --auth-user-pass credentials.txt


rsync -avz --progress "http://192.168.5.5:5000/volume1/CNLS/Data Science/ML/models in production" "/home/tom/DSML125/inputFiles"
