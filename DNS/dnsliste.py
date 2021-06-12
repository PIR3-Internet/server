import geoip2.database
import geoip2.errors
import dns.resolver
import csv
import sqlite3
import alexa

errors = 0
compteur = 1

def get_ns_url(domain):
    global errors
    try:
        response = dns.resolver.resolve(domain, 'NS')
        NSlist = [res.to_text() for res in response]
        return NSlist
    except dns.resolver.NoAnswer:
        print("Pas de réponse DNS pour ce domaine : ", domain)
        errors += 1
    except dns.exception.Timeout:
        print(f"Timeout for {domain}")
        errors += 1
    except dns.resolver.NXDOMAIN:
        print(f"DNS query name does not exist: {domain}")
        errors += 1
    except dns.resolver.NoNameservers:
        print(f"No response for: {domain}")
        errors += 1
    return []


def get_ip_ns(NS):
    global errors
    try:
        result = dns.resolver.resolve(NS, 'A')
        IP = result[0].to_text()
        return IP
    except dns.resolver.NoAnswer:
        print(f"Pas de réponse IP pour dns : {NS}")
        errors += 1
    except dns.exception.Timeout:
        print(f"Timeout pour DNS Request : {NS}")
        errors += 1
    except dns.resolver.NXDOMAIN:
        print(f"DNS name does not exist for {NS}")
        errors += 1
    except dns.resolver.NoNameservers:
        print(f"No response for: {NS}")
        errors += 1
    return None


def get_asn_from_ip(IP, orgList):
    global errors
    with geoip2.database.Reader('./GeoLite2-ASN/GeoLite2-ASN.mmdb') as reader:
        try:
            answer = reader.asn(IP)
            print(answer.autonomous_system_organization)
            if answer.autonomous_system_organization not in orgList:
                orgList.append(answer.autonomous_system_organization)
        except geoip2.errors.AddressNotFoundError:
            print('IP not in Database')
            errors += 1
        except ValueError:
            print("Problème avec l'IP")
            errors += 1


def insert_db(domain, orgList, rank):
    for item in orgList:
        c.execute('''INSERT INTO DNS(URL, NS, RANK) VALUES(?, ?, ?)''', (str(domain), item, rank))
        conn.commit()


def liste_db(cursor):
    liste = []
    cursor.execute('''SELECT URL FROM DNS''')
    for url in cursor:
        liste.append(url[0])
    return liste


if __name__ == "__main__":

    conn = sqlite3.connect('dns.db')
    c = conn.cursor()

    conn.execute('''CREATE TABLE if not exists DNS
             (URL TEXT NOT NULL,
             NS TEXT,
             RANK INT);''')

    db = liste_db(c)
    print(db)

    rank = 0
    Alexa = alexa.Alexa('list1m2020.csv')
    domainList = Alexa.retrieve_top(10000)
    for domain in domainList:
        rank += 1
        if domain not in db:
            orgList = []
            NSList = get_ns_url(domain)
            if len(NSList) != 0:
                for NS in NSList:
                    IP = get_ip_ns(NS)
                    if IP != None:
                        get_asn_from_ip(IP, orgList)
                insert_db(domain, orgList, rank)
        else:
            print(f"{domain} already in db")



    print("Fin de recherche")
    print(f"{errors} sites n'ont pas donnés de réponses")









