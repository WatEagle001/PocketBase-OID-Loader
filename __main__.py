from pocket_base_connector import PocketBaseClient
import json

client = PocketBaseClient("andrea.veronese@lantechlongwave.it","")
client._user_auth()

file = open('db_oid.json')
dati = json.load(file)

vendor = ["cisco", "vmware", "pfsense", "linux","allot", "ibm", "f5","bluecoat","extreme networks", "alcatel-lucent",  "checkpoint", "dell", "forcepoint", "aruba", "fortinet", "huawei", "hp"]
services = ["cpu", "fan", "ram", "disk", "temperature", "psu", "stack_member_status"]

for ven in vendor:
    for serv in services:
        if serv in dati[ven]:
            if len(dati[ven][serv]["oids"]) > 1:
                for indice in range(len(dati[ven][serv]["oids"])):
                    client.save_sqs_message(ven,serv,dati[ven][serv]["oids"][int(indice)])
            else:
                client.save_sqs_message(ven,serv,dati[ven][serv]["oids"][0])