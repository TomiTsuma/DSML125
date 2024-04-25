#!/bin/bash

if ! command -v openvpn &> /dev/null; then
    sudo apt install openvpn
fi

connect_to_vpn() {
    sudo openvpn --config /home/tom/DSML125/sslvpn-tsuma-client-config.ovpn --auth-user-pass credentials.txt &
    echo "Connecting to VPN..."
    sleep 10 # Adjust sleep time as needed for the connection to establish
    echo "VPN connected successfully."
}

# Main function
main() {
    echo "Starting VPN connection..."
    connect_to_vpn
}

# Execute main function
main