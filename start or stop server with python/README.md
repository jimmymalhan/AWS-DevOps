## Deployement Instructions

* Run the script to manually `Start_up and Shutdown or Reboot` instances when required.

## Prerequisites:
```
* aws configure setup for cli v2
* python, boto3, OS, sys, time,future
* Make sure your OS already satisfy the requirements.
```
## Example: (command varies by OS)
```
* apt-get install -y python-future (command for ubuntu)
* chmod a+x on_demand_startup_instances.py
* pip install boto3 (command for windows)
```
## Run the script:
* region = your_region
* python on_demand_startup_instances.py

