import dns.query
import geoip2.database
import geoip2.errors
import sqlite3

import whois

conn = sqlite3.connect('database.db')
c = conn.cursor()

conn.execute('''CREATE TABLE if not exists DNS
         (URL TEXT NOT NULL,
         NS TEXT);''')

print("Entrez un nom de domaine : ")
domain = input()
name_server = '1.1.1.1'
orgList = []
orgTemp = None
alreadyHere = False

"""
cursor = conn.execute('''SELECT URL from DNS''')
for url in cursor:
    urlFormated = url[0][:-1]
    if domain == urlFormated:
        print("Already in Database")
        alreadyHere = True
"""
if not alreadyHere:
    domain = dns.name.from_text(domain)

    request = dns.message.make_query(domain, dns.rdatatype.NS)
    response = dns.query.udp(request, name_server)
    NSlist = list(response.answer[0].items.keys())
    print(len(NSlist))
    for NS in NSlist:
        print(NS.to_text())
        dns_domain = dns.name.from_text(NS.to_text())
        request_dns = dns.message.make_query(dns_domain, dns.rdatatype.A)
        IP_response = dns.query.udp(request_dns, name_server)
        IPList = list(IP_response.answer[0].items.keys())
        IP = IPList[0]
        print(IP.to_text())
        with geoip2.database.Reader('./GeoLite2-ASN/GeoLite2-ASN.mmdb') as reader:
            try:
                answer = reader.asn(IP.to_text())
                print(answer.autonomous_system_organization)
                if answer.autonomous_system_organization != orgTemp:
                    if answer.autonomous_system_organization[:2] == "AS" and answer.autonomous_system_organization[3:].isdigit():
                        whoisQuery = whois.query(answer.autonomous_system_organization)
                        print(whoisQuery.__dict__)
                    else:
                        orgList.append(answer.autonomous_system_organization)
                orgTemp = answer.autonomous_system_organization
            except geoip2.errors.AddressNotFoundError:
                print('IP not in Database')
            except ValueError:
                print("Problème avec l'IP")
                pass
    """
    for item in orgList:
        c.execute('''INSERT INTO DNS(URL, NS) VALUES(?, ?)''', (str(domain), item))
        conn.commit()
"""
