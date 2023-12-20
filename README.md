#gate_api_automation

I was commissioned to make an executable with GUI that runs at a commercial venue and controls a specific gate on the network.

The purpose of the program is to allow customers to scan their ID on a barcode reader, for that ID to then be processed with an API through their internal backend system and sign them in, as well as make another HTTPS api call opening the gates.

The GUI continuously listens for ID input and handles any errors on its own, it also resets every 24hrs to avoid any bloating, as such it is completely self sufficient, it just needs to be run on a computer within the network.

The api calls have been anonimized for security. 

This project is currently successfully deployed.
