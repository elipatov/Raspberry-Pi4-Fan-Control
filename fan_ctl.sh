#! /bin/sh

### BEGIN INIT INFO
# Provides:          fan_ctl.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting fan_ctl_12v.py"
    /opt/fan-ctl/fan_ctl_12v.py &
    ;;
  stop)
    echo "Stopping fan_ctl_12v.py"
    pkill -f /opt/fan-ctl/fan_ctl_12v.py
    ;;
  *)
    echo "Usage: /etc/init.d/fan_ctl.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
