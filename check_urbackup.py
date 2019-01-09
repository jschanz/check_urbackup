
#!/usr/bin/env python3
#
# Written By:Tal Bar-Or'
# Created - 21/12/2016
#
# check_urbackup for backup status
#
#Ver 0.3import urbackup_api
#simple script to check Urbackup backup status used by https://github.com/uroni/urbackup-server-python-web-api-wrapper
#source code found at https://bitbucket.org/tal_bar_or/check_urbackup
#
# Updated 31.12.2018 11:48
# Jens Schanz <jens@schanz.cloud>
# https://github.com/jschanz/check_urbackup
#
# 1.0 Initial version by Tal Bar-Or
# 1.1 Readability of output improved and perfdata added by Jens Schanz
#
import urbackup_api
import datetime,sys
import time,argparse

ClientPrint = ""
Perfdata_OK = 0
Perfdata_WARNING = 0
Perfdata_CRITICAL = 0
GlobalStatus = []
Globelstat = ""

def Statuscheck(client):
    global ClientPrint
    global Perfdata_OK
    global Perfdata_WARNING
    global Perfdata_CRITICAL
    ClientStatus = ""
    if client["delete_pending"] != 0 and client["file_ok"] == True and client["online"] == True:
        ClientStatus = "OK"
        ClientPrint += client["name"] +"\n\t -> Client Status: Online" +"\n\t -> Last Backup: "+ datetime.datetime.fromtimestamp(client["lastbackup"]).strftime("%d.%m.%Y %X") \
              +"\n\t -> Backup Status: OK"+"\n\t -> Status: OK" +'\n'
        Perfdata_OK = Perfdata_OK + 1
        return ClientStatus

    elif client["delete_pending"] != 0 and client["file_ok"] != True and client["online"] == True:
        ClientStatus = "Critical"
        ClientPrint += client["name"] + "\n\t -> Client Status: Online" + "\n\t -> Last Backup: " + datetime.datetime.fromtimestamp(client["lastbackup"]).strftime("%d.%m.%Y %X") \
                       + "\n\t -> Backup Status: CRITICAL"+"\n\t -> Status: ***!!! CRITICAL !!!***" + '\n'
        Perfdata_CRITICAL = Perfdata_CRITICAL + 1
        return ClientStatus

    elif client["delete_pending"] != 0 and client["file_ok"] != True and client["online"] != True:
        ClientStatus = "Critical"
        ClientPrint += client["name"] + "\n\t -> Client Status: Down" + "\n\t -> Last Backup: " + datetime.datetime.fromtimestamp(client["lastbackup"]).strftime("%d.%m.%Y %X") \
                       + "\n\t -> Backup Status: CRITICAL" +"\n\t -> Status: ***!!! CRITICAL !!!***"+ '\n'
        Perfdata_CRITICAL = Perfdata_CRITICAL + 1
        return ClientStatus

    elif client["delete_pending"] != 0 and client["file_ok"] == True and client["online"] != True:
        ClientStatus = "Warning"
        ClientPrint += client["name"] + "\n\t -> Client Status: Down" + "\n\t -> Last Backup: " + datetime.datetime.fromtimestamp(client["lastbackup"]).strftime("%d.%m.%Y %X") \
                       + "\n\t -> Backup Status: OK" +"\n\t -> Status: WARNING" + '\n'
        Perfdata_WARNING = Perfdata_WARNING + 1
        return ClientStatus

parser = argparse.ArgumentParser()
parser.add_argument('--version','-v',action="store_true",help='show agent version')
parser.add_argument('--host','-ho',action="append",help='host name or IP')
parser.add_argument('--user','-u',action="append",help='User name for Urbackup server')
parser.add_argument('--password','-p',action="append",help='user password for Urbackup server')
args = parser.parse_args()

if args.host or args.user or args.password:
    try:
        server = urbackup_api.urbackup_server("http://"+ args.host[0] +":55414/x", args.user[0], args.password[0])
        clients = server.get_status()
        for client in clients:
            GlobalStatus.append(Statuscheck(client))
            Globelstat = set(GlobalStatus)
        while True:
            if "Critical" in Globelstat:
                #print(Globelstat)
                print("CRITICAL: There are " + str(Perfdata_CRITICAL) + " Backups in state CRITICAL \n\t-> OK:" + str(Perfdata_OK) + " WARNING:" + str(Perfdata_WARNING) + " CRITICAL:" + str(Perfdata_CRITICAL) + "\n")
                exitCode = 2
                break
            elif "Warning" in Globelstat:
                #print(Globelstat)
                print("WARNING: There are " + str(Perfdata_WARNING) + " Backups in state WARNING \n\t-> OK:" + str(Perfdata_OK) + " WARNING:" + str(Perfdata_WARNING) + " CRITICAL:" + str(Perfdata_CRITICAL) + "\n")
                exitCode = 1
                break
            elif "OK" in Globelstat:
                #print(Globelstat)
                print("OK: There are " + str(Perfdata_OK) + " Backups in state OK \n\t-> OK:" + str(Perfdata_OK) + " WARNING:" + str(Perfdata_WARNING) + " CRITICAL:" + str(Perfdata_CRITICAL) + "\n")
                exitCode = 0
                break
            else:
                print("UNKOWN: Please check manually, why state is Unknown")
                exitCode = 3
                break

        print(ClientPrint)
        print ("| OK=" + str(Perfdata_OK) + ";;" + " WARNING=" + str(Perfdata_WARNING) + ";;" + " CRITICAL=" + str(Perfdata_CRITICAL) + ";;")
        sys.exit(exitCode)

    except Exception as e:

        print("Error Occured: ",e)


elif args.version:
    print('1.1 Urback Check ,Written By:Tal Bar-Or')
    sys.exit()
else:
    print("please run check --host <IP OR HOSTNAME> --user <username> --password <password>"+ '\n or use --help')
    sys.exit()
