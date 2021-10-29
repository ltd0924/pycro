# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
from pycromanager import Bridge


mmcore_dir="G:\Micro-Manager-2.0\ImageJ.exe";
#os.system(mmcore_dir)
#暂时无法使用，调用后无法完全启动
#Create the Micro-Managert to Pycro-Manager transfer layer
bridge = Bridge()
#get object representing micro-manager core
core = bridge.get_core()

deviceList = core.get_loaded_devices()

#打印loaded device 的属性
for i in range(deviceList.size()):
    print(deviceList.get(i))
    acc=core.get_device_property_names(deviceList.get(i))
    for j in range(acc.size()):
        print(acc.get(j),core.get_property(deviceList.get(i),acc.get(j)))
    print('\n')

#Laser 为例
core.set_property("Toptica_iBeamSmartCW","LASER_OPERATION","On")
core.set_property("Toptica_iBeamSmartCW","Power(mW)",3.00)


