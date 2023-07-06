#RealTime_Monitor_PLC_Python_Socket_HTML

python Client.py  (Keep prompt PLC address output 100)

Then 

Python Backend 

Run python RealTimeMonitorPLCAddressSocketServer.py

When there is index.html run, This python Backend will receive data from the PLC

index.html is subscribing RealTimeMonitorPLCAddressSocketServer.py socket therefore it can be real time however there is some latency 

