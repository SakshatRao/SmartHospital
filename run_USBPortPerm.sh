#!/usr/bin/bash

user_name=$1

# Giving USB port permissions
user_id=$(id -u)
if [[ $user_id -eq 0 ]];
then
    sudo chown ${user_name} /dev/ttyUSB0
    sudo chown ${user_name} /dev/ttyACM0
    echo "Permissions to USB ports granted!"
    exit
else
    echo "Root privileges do not exist!"
fi