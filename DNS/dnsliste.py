import geoip2.database
import geoip2.errors
import dns.query
import csv
import sqlite3
import whois

name_server = '1.1.1.1'
domainList = []

conn = sqlite3.connect('database.db')
c = conn.cursor()

conn.execute('''CREATE TABLE if not exists DNS
         (URL TEXT NOT NULL,
         NS TEXT);''')

f = open(r"list1m2020.csv")
myReader = csv.reader(f)

for row in myReader:
    ligne = row[0]
    domainList.append(ligne)

domainList = domainList[:1000]
print(domainList)

for domain in domainList:
    orgList = []
    orgTemp = None
    domain = dns.name.from_text(domain)
    alreadyHere = False

    if not alreadyHere:
        request = dns.message.make_query(domain, dns.rdatatype.NS)
        response = dns.query.udp(request, name_server)
        try:
            NSlist = list(response.answer[0].items.keys())
        except IndexError:
            print("Pas de réponse DNS pour ce domaine : ", domain)
            continue
        # print(len(NSlist))
        for NS in NSlist:
            # print(NS.to_text())
            dns_domain = dns.name.from_text(NS.to_text())
            request_dns = dns.message.make_query(dns_domain, dns.rdatatype.A)
            IP_response = dns.query.udp(request_dns, name_server)
            try:
                IPList = list(IP_response.answer[0].items.keys())
                IP = IPList[0]
                print(IP.to_text(), " / ", domain)
                with geoip2.database.Reader('./GeoLite2-ASN/GeoLite2-ASN.mmdb') as reader:
                    try:
                        answer = reader.asn(IP.to_text())
                        print(answer.autonomous_system_organization)
                        if answer.autonomous_system_organization != orgTemp:
                            orgList.append(answer.autonomous_system_organization)
                        orgTemp = answer.autonomous_system_organization
                    except geoip2.errors.AddressNotFoundError:
                        print('IP not in Database')
                    except ValueError:
                        print("Problème avec l'IP")
            except IndexError:
                pass
        for item in orgList:
            c.execute('''INSERT INTO DNS(URL, NS) VALUES(?, ?)''', (str(domain), item))
            conn.commit()

print("Fin de recherche")
