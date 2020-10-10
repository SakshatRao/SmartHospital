# Uploading lua scripts to NodeMCU

1. (Optional) Ensure /dev/ttyUSB0 has user permissions

    ```python
    sudo su
    chown <username> /dev/(ttyUSB0/ttyACM0)
    exit
    ```

2. Switch to Python2

    ```python
    conda activate python2
    ```

3. (Optional) Upload NodeMCU firmware

    ```python
    esptool.py --port=/dev/(ttyUSB0/ttyACM0) write_flash -fm=dio -fs=32m 0x00000 nodemcu-master-(...).bin
    ```

4. Upload lua scripts to NodeMCU

    (Optional) Ensuring Mosquitto is not enabled

    ```python
    ps -ef | grep mosquitto
    sudo kill <process id>
    ```

    (Optional) Clearing serial port

    ```python
    miniterm.py /dev/(ttyUSB0/ttyACM0) 115200
    CNTRL+]
    ```

    Uploading of lua scripts

    ```python
    python luatool.py --port /dev/(ttyUSB0/ttyACM0) --baud 115200 --src <file>.lua --verbose
    ```
