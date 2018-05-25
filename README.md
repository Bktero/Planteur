# Planteur

_Planteur_ is a system for automatic plant monitoring and watering.

## Python
### Modules
Install using pip(3):
 
 - paho-mqtt https://pypi.org/project/paho-mqtt
 - pyserial http://pyserial.readthedocs.io/en/latest/shortintro.html


## MQTT
### Mosquitto as message broker
`sudo apt install mosquitto`

### Topics and messages
For all messages, timestamp is the number of seconds since the Unix Epoch.

Mosquitto provides 'pub'/'sub' clients:
`sudo apt install mosquitto-clients`
 
Use the 'sub' client to watch all topics from a terminal:
`$ mosquitto_sub -h localhost -t 'planteur/ambient' -t 'planteur/plant' -t 'planteur/watering'`

### plant/ambient
`{"ambient": {"timestamp": 1527020566.8461428, "uid": "cellier", "humidity": 18, "temperature": 80}}`

`{"ambient": {"timestamp": 1527020566.8507495, "uid": "living-room", "temperature": 18}}`

`{"ambient": {"timestamp": 1527020566.8536906, "uid": "cave", "humidity": 75}}`
 
Humidity and temperature are optional but at least one of them but be present.

 
#### plant/plant
`{"plant": {"timestamp": 1527020566.8409116, "uid": "pilea", "humidity": 80}}`

`{"plant": {"timestamp": 1527020566.844942, "uid": "cactus", "humidity": 50, "temperature": 25}}`

Humidity is mandatory while temperature is optional.

####plant/watering
`{"watering": {"timestamp": 1527020566.8558247, "uid": "pilea"}}`

`{"watering": {"timestamp": 1527020566.8568103, "uid": "cactus"}}`


## Links
Online JSON validator | [http://jsonlint.com/](http://jsonlint.com/)

Markdown Cheatsheet | [https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
