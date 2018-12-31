# check_urbackup

Simple script to check Urbackup backup status ,based on https://github.com/uroni/urbackup-server-python-web-api-wrapper
You will need to have Pythone3.x installed and pip3 install urbackup-server-web-api-wrapper prior to usage.

## Installation
```bash
pip3 install urbackup-server-web-api-wrapper
```

## Usage

usage: check_urbackup.py [-h] [--version] [--host HOST] [--user USER]
                         [--password PASSWORD]

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show agent version
  --host HOST, -ho HOST
                        host name or IP
  --user USER, -u USER  User name for Urbackup server
  --password PASSWORD, -p PASSWORD
                        user password for Urbackup server

## Example

Create a new user in the web ui and execute the following command

```bash
'/usr/bin/python3' '/usr/lib/nagios/plugins/check_urbackup.py' '--host' 'urbackup.host.domain' '--password' 'vaitee4Gi2iex2meengaoqu6' '--user' 'icinga2'
```
### Icinga2 Output
![Urbackup Icinga2](https://raw.githubusercontent.com/jschanz/check_urbackup/master/img/urbackup_icinga2.png)

### Icinga2 Perfdata (Grafana)
![Urbackup Perfdata (Grafana)](https://raw.githubusercontent.com/jschanz/check_urbackup/master/img/urbackup_perfdata.png)
