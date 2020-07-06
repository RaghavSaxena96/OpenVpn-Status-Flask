import sys
import os
from flask import Flask
from flask import render_template,flash,redirect,request
import datetime
from openvpn_status import parse_status
import collections
import json
import IP2Location
 
IP2LocObj = IP2Location.IP2Location()


IP2LocObj.open("data/IP-COUNTRY.BIN")
rec = IP2LocObj.get_all("3.7.69.254")

print(rec.country_short)
print(rec.country_long)
print(rec.region)
print(rec.city)


'''

#   Status Object------------------------------

print('\n------------------------Status Object---------------------------\n')

print(dir(status))
print('\n------------------------Status Properties-----------------------------\n')
print(status.__dict__)




#------------------Routing Table----------------------------

print('\n-----------------------Routing Table Items----------------------\n')

for item in routing.items():
   print(item)




#----------------Client_list--------------------------------

print('\n--------------Client List items---------------------\n')

for item in client_dict.items():
	print(item)



#--------------------Global_Stats---------------------------

print('\n----------------------Global_Stats--------------------------------\n')

print(dir(global_stats))

#-------------------------------Updated at----------------------------------------

print('\n---------------------Updated at------------------------------------\n')

print('Updated at time  '+str(status.updated_at)+'\n')

'''



#----------------------------Server 1-----------------------------------------------------------------

print('\n--------------------------Server 1 data -------------------------------------------\n')

with open('openvpn-status.log') as logfile:
    status = parse_status(logfile.read())


clients = status.client_list
client_dict=status.client_list
global_stats1=status.global_stats
routing=status.routing_table


#----------------------------Client List Creation -----------------------------------

print(clients.__dir__)



od = collections.OrderedDict(sorted(client_dict.items(), key=lambda x:x[1]))
print(od)



clients_list = [i for i in od.keys()]

client_ip=[]
client_port=[]
client_name=[]
client_connect=[]
client_bytesend=[]
client_bytereceived=[]
client_country=[]


# Cannot convert to json as IPV4 Address is not serializable

for client in clients_list:
	foo_client = status.client_list[client]
	print(foo_client.__dict__)
	#json_str = json.dumps(foo_client.__dict__)
	#print(json_str)
	client_ip.append(foo_client.real_address.host)
	client_port.append(foo_client.real_address.port)
	client_name.append(foo_client.common_name)
	client_connect.append(foo_client.connected_since)
	print(foo_client.common_name)  
	client_bytereceived.append(foo_client.bytes_received)  
	client_bytesend.append(foo_client.bytes_sent)
	ip=str(foo_client.real_address.host)
	print(ip)
	rec1 = IP2LocObj.get_all(ip)
	client_country.append(rec1.country_long)
	print(rec1.country_long)


updated1=str(status.updated_at)

print(updated1)


#-----------------------------------------Server2-------------------------------------------------------

print('\n--------------------------Server 2 data -------------------------------------------\n')

with open('openvpn2-status.log') as logfile:
    status = parse_status(logfile.read())

client_dict=status.client_list
global_stats2=status.global_stats
routing=status.routing_table

od = collections.OrderedDict(sorted(client_dict.items(), key=lambda x:x[1]))
print(od)


clients_list = [i for i in od.keys()]
client_ip2=[]
client_port2=[]
client_name2=[]
client_connect2=[]
client_bytesend2=[]
client_bytereceived2=[]
client_country2=[]


for client in clients_list:
	foo_client2=status.client_list[client]
	client_ip2.append(foo_client2.real_address.host)
	client_port2.append(foo_client2.real_address.port)
	client_name2.append(foo_client2.common_name)
	client_connect2.append(foo_client2.connected_since)
	print(foo_client.common_name)  
	client_bytereceived2.append(foo_client.bytes_received)  
	client_bytesend2.append(foo_client.bytes_sent)  
	print(int(foo_client.bytes_sent))
	rec = IP2LocObj.get_all(str(foo_client.real_address.host))
	client_country2.append(rec.country_long) 


updated2=str(status.updated_at)

print(updated2)


print(status.__dict__)

print(global_stats2.__dict__)
#-------------------------------------API End Points--------------------------------------------

app = Flask(__name__)


@app.route('/')
def home():
	return render_template("index.html",server1_status = updated1,server2_status = updated2,gs1 = global_stats1.max_bcast_mcast_queue_len ,gs2 = global_stats2.max_bcast_mcast_queue_len)


@app.route('/logs')
def loger():
	return 'Clients Logs'



@app.route('/updatedat')
def updater():
	return str(status.updated_at)


@app.route('/client1')

def client_lister1():
	return render_template("client2.html",update = updated1,server = 'Server 1' , len = len(client_ip),country = client_country, Clients = client_ip,Port = client_port,Name = client_name,connect = client_connect,bsend=client_bytesend,breceived=client_bytereceived) 



@app.route('/client2')

def client_lister2():
	return render_template("client2.html",update = updated2, server = 'Server 2',len = len(client_ip2),country = client_country2 , Clients = client_ip2,Port = client_port2,Name = client_name2,connect = client_connect2,bsend=client_bytesend2,breceived=client_bytereceived2)



if __name__ == '__main__':
	# -------to run for a public ip ------------
	# app.run(host='3.7.69.254',port=8085)
	app.run(debug=True)
