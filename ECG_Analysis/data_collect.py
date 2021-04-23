# stage1.py
import time
import random
import numpy as np

class DataCollect:

    def data_collect(self, queueS1, queueS2):
        while(True):
            if not queueS2.empty():
                msg = queueS2.get()    # get msg from s2
                if(len(msg) == 0):
                    break
                yield msg
            time.sleep(3)
            queueS1.put("Next")
        queueS1.put("Stop")