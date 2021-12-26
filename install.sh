#! /bin/sh

set -e

echo "=> Installing fan controller...\n"
sudo mkdir /opt/fan-ctl/
sudo cp fan_ctl_12v.py /opt/fan-ctl/
sudo chmod +x /opt/fan-ctl/fan_ctl_12v.py

echo "=> Starting fan controller...\n"
sudo cp fan_ctl.sh /etc/init.d/
sudo chmod +x /etc/init.d/fan_ctl.sh

sudo update-rc.d fan_ctl.sh defaults
sudo /etc/init.d/fan_ctl.sh start

echo "Fan controller installed."
