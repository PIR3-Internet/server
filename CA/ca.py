import ssl
import socket
import OpenSSL
from pprint import pprint
from datetime import datetime
import sqlite3
import signal
from functools import wraps


class TimeoutException(Exception):
    pass

def deadline(timeout, *args):
    def decorate(f):
        def handler(signum, frame):
            raise TimeoutException()        #when the signal have been handle raise the exception
        
        @wraps(timeout, *args)
        def new_f(*args):
            signal.signal(signal.SIGALRM, handler)      #link the SIGALARM signal to the handler
            signal.alarm(timeout)                       #create an alarm of timeout second
            res = f(*args)

            signal.alarm(0)                             #reinitiate the alarm
            return res

        #new_f.__name__ = f.__name__

        return new_f
    return decorate



@deadline(15)
def get_certificate(host, port=443, timeout=10):
    context = ssl.create_default_context()
    conn = socket.create_connection((host, port))
    sock = context.wrap_socket(conn, server_hostname=host)
    sock.settimeout(timeout)
    try:
        der_cert = sock.getpeercert(True)
    finally:
        sock.close()
    return ssl.DER_cert_to_PEM_cert(der_cert)


#def store_certificates():
    



#if __name__ == '__main__':
con = sqlite3.connect('ca-providers.db')
cur = con.cursor()
try:
    cur.execute("create table ca (ca_user, ca_provider)")
except sqlite3.OperationalError:
    cur.execute("DELETE FROM ca")

with open("list1m2020.csv", "r") as f:
    for line in f:

        counter = 0
        ok = False

        user = line.split()[0]

        while ok == False:
            try:
                certificate = get_certificate(user)
                x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)

                provider = x509.get_issuer().organizationName#{
                                #'subject': dict(x509.get_subject().get_components()),
                                #'issuer': dict(x509.get_issuer().get_components()),
                                #'serialNumber': x509.get_serial_number(),
                                #'version': x509.get_version(),
                                #'notBefore': datetime.strptime(x509.get_notBefore(), '%Y%m%d%H%M%SZ'),
                                #'notAfter': datetime.strptime(x509.get_notAfter(), '%Y%m%d%H%M%SZ'),
                            #}

                            #extensions = (x509.get_extension(i) for i in range(x509.get_extension_count()))
                            #extension_data = {e.get_short_name(): str(e) for e in extensions}
                            #result.update(extension_data)

                cur.execute("insert into ca values (?, ?)", (user, provider))
                con.commit()

                print(user, ": ", provider)

                ok = True
            
            except TimeoutException:
                print("     TimeoutException for ", user)
                ok = False
                counter += 1
            except OSError:
                print("     No route to ", user)
                ok = False
                counter += 1
            
            except BlockingIOError:
                print("     BlockingIOError from ", user)
                ok = False
                counter += 1
            except socket.gaierror:
                print("     No address associated with ", user)
                ok = True
            except ConnectionRefusedError:
                print("     Connection with ", user, " refused")
                ok = False
                counter += 1
            except ssl.CertificateError:
                print("     ", user, " haven't got any certificate")
                ok = True
            except ssl.SSLError:
                print("     certificate verify failed for ", user)
                ok = False
                counter += 1
            
            if counter == 1:
                ok = True

con.close()