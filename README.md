#RealTime_Monitor_PLC_Python_Socket_HTML

python Client.py  (Keep prompt PLC address output 100)

Then 

Python Backend 

Run python RealTimeMonitorPLCAddressSocketServer.py

When there is index.html run, This python Backend will receive data from the PLC

index.html is subscribing RealTimeMonitorPLCAddressSocketServer.py socket therefore it can be real time however there is some latency 


INPUT: 

0.03

0.05

0.07

0.09


OUTPUT:

100.00

100.01

100.02

100.03 (Alaram)

Hardware Overview:

![image](https://github.com/junxian428/RealTime_Monitor_PLC_Python_Socket_HTML/assets/58724748/92640cb5-8b75-491a-b6bc-ba75400953f9)



PLC program

![image](https://github.com/junxian428/CP1E_Wiring_Diagram/assets/58724748/f833adc9-8c18-4b1d-8685-636877fa8058)


Backend: 

Python

Platform：

Raspberry Pi

Connector:

OMRON CP1E to USB convertor


Method:

C-Command



Real Time Tech:

Socket 



Frontend:

HTML



Wiring Diagram:

![Untitled Diagram drawio (4)](https://github.com/junxian428/RealTime_Monitor_PLC_Python_Socket_HTML/assets/58724748/e2946f97-5772-4616-8143-2095a8536f34)




