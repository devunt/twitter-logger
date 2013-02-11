twitter-logger
==============

Twitter logging script (written in python 2.7)

## How to Use
1. Copy config.tmpl.ini to config.ini
2. Run logger.py

### how to run as daemon
#### use screen
$ screen -dmS twitter-logger python log.py

#### use nohup
$ nohup python log.py &
