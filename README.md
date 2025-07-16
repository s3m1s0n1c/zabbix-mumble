# zabbix-mumble
Zabbix python script to get stats from Mumble-Server 1.5

We assume you have zabbix-agent/zabbix-agent2 already installed - If not Zabbix Agent2 install documentation below:

https://www.zabbix.com/download?zabbix=7.4&os_distribution=ubuntu&os_version=22404&components=agent_2&db=&ws=

# Install Dependencies for script

`sudo apt install zeroc-ice-all-dev python3-zeroc-ice git`

# Install Zabbix-Mumble Script

`git clone https://github.com/s3m1s0n1c/zabbix-mumble.git`

`cd zabbix-mumble`

`sudo mkdir /usr/share/slice`

`sudo cp MumbleServer.ice /usr/share/slice`

`sudo mkdir -p /usr/local/scripts/zabbix`

`sudo cp zabbix-mumble.py /usr/local/scripts/zabbix`

`sudo chown -R zabbix:zabbix /usr/local/scripts/zabbix`

`sudo chmod u+x /usr/local/scripts/zabbix/zabbix-mumble.py`

`sudo cp userparameter_mumble.conf /etc/zabbix/zabbix_agent2.d/` (Agent2) or `sudo cp userparameter_mumble.conf /etc/zabbix/zabbix_agent.d/` (Agent)

`sudo service zabbix-agent2 restart` or `service zabbix-agent restart`

# Install Zabbix-Mumble Template in Zabbix

Download mumblestats_template.yaml to your PC and import to zabbix
Add "Mumble Stats" template to host

Mumble Stats should now propergate for that zabbix host


