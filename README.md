#RealTime_Monitor_PLC_Python_Socket_HTML

python Client.py  (Keep prompt PLC address output 100)

Then 

Python Backend 

Run python RealTimeMonitorPLCAddressSocketServer.py


Frontend

node express.js

Database SQLite:

Debian: sudo apt-get install sqlitebrowser

sqlitebrowser


CREATE TABLE "PLC" (

	"id"	INTEGER,

	"address_0"	TEXT,

	"address_1"	TEXT,

	"address_2"	TEXT,

	"address_3"	TEXT,

	"address_4"	TEXT,

	"address_5"	TEXT,

	"address_6"	TEXT,

	"address_7"	TEXT,

	"address_8"	TEXT,

	"address_9"	TEXT,

	"address_10"	TEXT,

	"address_11"	TEXT,

	"address_12"	TEXT,

	"address_13"	TEXT,

	"address_14"	TEXT,

	"address_15"	TEXT,

	PRIMARY KEY("id" AUTOINCREMENT)
    
);




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




