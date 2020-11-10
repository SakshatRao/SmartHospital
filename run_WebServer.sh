#!/usr/bin/bash

if [[ $1 == "USBPerm" ]];
then
    user_name=$(whoami)
    sudo ./run_USBPortPerm.sh ${user_name}
fi
# Starting the mosquitto broker
mosquitto -d

# Activating project environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate SmartHospitalPython

# Running following commands in parallel
#   1. Running web-server
#   2. Opening website
#   3. Running data-logger file
(cd SmartHospitalServer/ && python3 manage.py runserver) &
(sleep 5 && xdg-open http://127.0.0.1:8000/) &
python3 data_logger.py &