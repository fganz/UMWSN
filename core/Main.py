from core import WebInterfaceController, SensorController, EventController
from core import SensorController

__author__ = 'frieder'





SensorController.start()
WebInterfaceController.start()
EventController.Watchdog(1).start()




#import matplotlib.pyplot as plt
#t1 = Series(getDictFromId(10))
#t2 = Series(getDictFromId(11))
#
#a1 = t1.plot()
#
#plt.show()
#print getSaxContinous("49",10)