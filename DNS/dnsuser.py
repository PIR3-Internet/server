import geoip2.database
import geoip2.errors
import dns.resolver
import csv
import sqlite3


def get_ns_url(domain):
    try:
        response = dns.resolver.resolve(domain, 'NS')
        NSlist = [res.to_text() for res in response]
        return NSlist
    except dns.resolver.NoAnswer:
        print("Pas de réponse DNS pour ce domaine : ", domain)
    except dns.exception.Timeout:
        print(f"Timeout for {domain}")
    except dns.resolver.NXDOMAIN:
        print(f"DNS query name does not exist: {domain}")
    except dns.resolver.NoNameservers:
        print(f"No response for: {domain}")
    return []


def get_ip_ns(NS):
    try:
        result = dns.resolver.resolve(NS, 'A')
        IP = result[0].to_text()
        return IP
    except dns.resolver.NoAnswer:
        print(f"Pas de réponse IP pour dns : {NS}")
    except dns.exception.Timeout:
        print(f"Timeout pour DNS Request : {NS}")
    except dns.resolver.NXDOMAIN:
        print(f"DNS name does not exist for {NS}")
    except dns.resolver.NoNameservers:
        print(f"No response for: {NS}")
    return None


def get_asn_from_ip(IP, orgList):
    with geoip2.database.Reader('./GeoLite2-ASN/GeoLite2-ASN.mmdb') as reader:
        try:
            answer = reader.asn(IP)
            print(answer.autonomous_system_organization)
            if answer.autonomous_system_organization not in orgList:
                orgList.append(answer.autonomous_system_organization)
        except geoip2.errors.AddressNotFoundError:
            print('IP not in Database')
        except ValueError:
            print("Problème avec l'IP")


def check_db(domain):
    c.execute('''SELECT COUNT(*) FROM DNS GROUP BY NS''')



if __name__ == "__main__":

    conn = sqlite3.connect('dns.db')
    c = conn.cursor()


    rank = 0
    print("Entrez un nom de domaine : ")
    domain = input()
    orgTemp = None
    orgList = []
    NSList = get_ns_url(domain)
    if len(NSList) != 0:
        for NS in NSList:
            IP = get_ip_ns(NS)
            if IP != None:
                get_asn_from_ip(IP, orgList)
    print(f"NS du groupe {orgList}")