# stage2.py
import time
import numpy as np
import pandas as pd
import serial

class SerialData:
    
    def __init__(self):

#         self.data = np.squeeze(pd.read_csv('../../Downloads/ecg_signals/ecg1.txt').values)
#         self.idx = 0

        pass

    def serial_data(self, queueS1, queueS2):
        while True:

#             msg = queueS1.get()    # wait till there is a msg from s1
#             if msg == 'Stop':
#                 break # ends loop
#             time.sleep(1) # work
#             queueS2.put(self.data[self.idx*1000: (self.idx+1)*1000])
#             self.idx += 1

            msg = queueS1.get()    # wait till there is a msg from s1
            if msg == 'Stop':
                break # ends loop
            serialPort = serial.Serial(
                port = "COM3",
                baudrate = 115200,
                bytesize = 8,
                timeout = 2,
                stopbits = serial.STOPBITS_ONE
            )
            values = []
            while(True):
                if(serialPort.in_waiting > 0):
                    serialString = serialPort.readline()
                    #serialString = "25"
                    val_str = serialString.decode('Ascii').strip()
                    try:
                        values.append(int(val_str))
                    except:
                        pass
                    if(len(values) > 2000):
                        #data = np.asarray(self.values)
                        queueS2.put(list(values))
                        serialPort.close()
                        break