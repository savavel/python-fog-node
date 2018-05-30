# python-fog-node

The Fog node represents an intermediary between cloud infrastructure and the edge devices (clients) of the network.
This new networking paradign was coined by Cisco, namely Fog & Edge Computing.

This implementation of a Fog network node can be installed in road-side infrastructure to support vehicular services.
It simulates a use case environment where vehicles (edge devices) connect to existing Cell tower infrastructure.
The og node is being hosted physically at the cell tower allowing for better latency and throughput.
The node does the processing locally, eliminating the need to communicate with cloud services.

It checks vehicle information such as speed, location and status and determines whether there is a collision and which vehicles participating in the network it should send a warning to.
