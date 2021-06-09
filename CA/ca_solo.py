#from Projet.server.ca import TIMEOUT
import ssl
import socket
from typing import final
import OpenSSL
from pprint import pprint
from datetime import datetime
import sqlite3
import signal
from functools import wraps
import requests


TIMEOUT = 90


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



@deadline(TIMEOUT)
def get_certificate(host, port=443, timeout=10):
    context = ssl.create_default_context()
    context.set_ciphers('DEFAULT:@SECLEVEL=1')
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    conn = socket.create_connection((host, port))
    sock = context.wrap_socket(conn, server_hostname=host)
    sock.settimeout(timeout)
    try:
        der_cert = sock.getpeercert(True)
    finally:
        sock.close()
    return ssl.DER_cert_to_PEM_cert(der_cert)


#def store_certificates():
    

@deadline(60)
def get_url(user):
    user = 'http://' + user
    user = requests.get(user).url.split('/')[2]
    return user

@deadline(60)
def get_url2(user):
    user = 'http://' + user
    user = requests.head(user).headers['location'].split('/')[2]
    return user

#if __name__ == '__main__':
user = 'jamnews.com' #'gamersky.com' #'wixsite.com' #input("url : ")


try:
    user = get_url(user)
except TimeoutException: 
    print("     Impossible to get url (TimeoutException) from ", user)
except: 
    try: 
        user = get_url2(user)
    except TimeoutException: 
        print("     Impossible to get url (TimeoutException) from ", user)
    except:
        print("     Impossible to get url from ", user)


counter = 0
cMax = 2
ok = False

while ok == False:
    try:
        certificate = get_certificate(user)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)

        provider = x509.get_issuer().organizationName

        print(user, ": ", provider)

        ok = True

                
    except TimeoutException as e:
        print("     ", repr(e), user)
        ok = False
        counter += 1

                
    except Exception as e:
        print("     ", repr(e), user)
        ok = False
        counter += 1
    
    if counter == cMax:
        ok = True