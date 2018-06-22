# cisco_config_push
A Python script to automate (non-critical) configuration pushes to Cisco routers via telnet
<p>
ips.txt should be formatted as follows for the script to read from it. Each host-credential triad should be in a new line in the following format. The fields are separated using a comma (,). </br>
[ip-address],[username],[password]</br>
[ip-address],[username],[password]
</p></br></br>
ex: </br>
192.168.10.133,user01,password123 </br>
192.168.10.199,user02,password123
