import datetime
import os
import subprocess
import telnetlib
import time


def executecommands():
    # router commands to be executed in the config terminal mode are given here.
    tn.write(b"ntp server 10.3.125.1" + b"\n")
    tn.read_until(b"#", 5)
    tn.write(b"clock timezone IST 05 30" + b"\n")
    tn.read_until(b"#", 5)
    tn.write(b"archive" + b"\n")
    tn.read_until(b"#", 5)
    tn.write(b"log config" + b"\n")
    tn.read_until(b"#", 5)



now = datetime.datetime.now()
buff = ''
resp = ''

# username and password for authentication when TACACS is used
username = "username"
unamepw = "password"

with open('ips.txt') as f:
    for line in f:
        line = line.strip()
        # telnet credential and ip extraction for remote login and authentication from ips.txt
        ip, telnetpw, enablepw = line.split(",")

        with open(os.devnull, "wb") as limbo:
            # check if host is up
            result = subprocess.Popen(["ping", "-n", "2", "-w", "1000", ip],
                                      stdout=limbo, stderr=limbo).wait()
            if result:
                print(ip, "Link Down - Site unreachable")
                f = open('DownSites.txt', 'a+')
                f.write(line + '\n')
                f.close()
            else:
                try:
                    response = ""
                    tn = telnetlib.Telnet(ip)
                    print("\n" + ip + " connected!")
                    time.sleep(2)

                    response = tn.read_until(b"username: ", 5)

                    if b"username:" in response:
                        tn.write(username.encode('ascii') + b"\n")
                        tn.read_until(b":", 5)
                        tn.write(unamepw.encode('ascii') + b"\n")
                        tn.read_until(b"#", 5)
                    else:
                        tn.write(telnetpw.encode('ascii') + b"\n")
                        tn.read_until(b">", 5)

                    tn.write(b"terminal length 0" + b"\n")
                    tn.read_until(b">", 5)
                    tn.write(b"enable" + b"\n")
                    tn.read_until(b"Password: ", 5)
                    tn.write(enablepw.encode('ascii') + b"\n")
                    tn.read_until(b"#", 5)
                    tn.write(b"conf ter" + b"\n")
                    tn.read_until(b"#", 5)

                    print("Init Complete!")

                    executecommands()

                    output = tn.read_all()
                    print(ip, "Reachable ~ Command Executed")
                    tn.close()
                    fp = open(ip + '.txt', "wb")
                    fp.write(output)
                    fp.close()
                except Exception as e:
                    print(ip, "ERROR: ", e)
