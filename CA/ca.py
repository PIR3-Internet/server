import ssl
import socket
import OpenSSL
import sqlite3
import signal
from functools import wraps
from numpy.core.numeric import count_nonzero
import requests
from multiprocessing import Process, Value

TIMEOUT = Value('i', 5)
cMax = Value('i', 2)
ca_num = Value('i', 0)
#table_exists = False

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

        return new_f
    return decorate



@deadline(TIMEOUT.value)
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


@deadline(60)
def url_direct(user):
    user = 'http://' + user
    user = requests.get(user).url.split('/')[2]
    return user

@deadline(60)
def url_with_header(user):
    user = 'http://' + user
    user = requests.head(user).headers['location'].split('/')[2]
    return user
    
def get_url(user, counter, error):
    try:
        user = url_direct(user)
    except TimeoutException: 
        print("     Impossible to get url (TimeoutException) from ", user)
        cur.execute("INSERT INTO errors VALUES (?, ?, ?)", (user, user.split('.')[len(user.split('.'))-1], error))
        counter = cMax.value-1
    except: 
        try: 
            user = url_with_header(user)
        except TimeoutException: 
            print("     Impossible to get url (TimeoutException) from ", user)
            cur.execute("INSERT INTO errors VALUES (?, ?, ?)", (user, user.split('.')[len(user.split('.'))-1], error))
            counter = cMax.value-1
        except:
            print("     Impossible to get url from ", user)
            cur.execute("INSERT INTO errors VALUES (?, ?, ?)", (user, user.split('.')[len(user.split('.'))-1], error))
            counter = cMax.value-1
    
    return user, counter


def processus(user):
    #con = sqlite3.connect('ca-providers2.db')
    #cur = con.cursor()

    counter = 0
    ok = False

    while ok == False:
        try:
            certificate = get_certificate(user)
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)

            provider = x509.get_issuer().organizationName

            cur.execute("INSERT INTO ca VALUES (?, ?, ?)", (user, provider, ca_num.value))

            print(user, ": ", provider)

            ok = True
                
        except TimeoutException as e:
            if (counter == cMax.value-1):
                if (TIMEOUT.value != 60):
                    TIMEOUT.value = 60
                    counter -= counter
                #elif (user != user_old):
                #    user = user_old
                #    counter -= counter
                else:
                    cur.execute("INSERT INTO errors VALUES (?, ?, ?)", (user, user.split('.')[len(user.split('.'))-1], repr(e)))
            else:
                user, counter = get_url(user, counter, repr(e))
            print("     ", repr(e), user)
            ok = False
            counter += 1

        except Exception as e:
            if (counter == cMax.value-1):
                cur.execute("INSERT INTO errors VALUES (?, ?, ?)", (user, user.split('.')[len(user.split('.'))-1], repr(e)))
            else:
                user, counter = get_url(user, counter, repr(e))
            print("     ", repr(e), user)
            ok = False
            counter += 1

        finally:
            con.commit()
            ca_num.value += 1
                
        if counter == cMax.value:
            ok = True
            


con = sqlite3.connect('ca-providers2.db')
cur = con.cursor()
try:
    cur.execute("CREATE TABLE ca (ca_user, ca_provider, ca_num)")
except sqlite3.OperationalError:
    cur.execute("DELETE FROM ca")
    #table_exists = True
    #cur.execute("SELECT MAX(ca_num) FROM ca")
    #ca_num.value = cur.fetchall()[0][0]
try:
    cur.execute("CREATE TABLE errors (user, extension, error)")
except sqlite3.OperationalError:
    cur.execute("DELETE FROM errors")

#con.close()
con.commit()

debut = 0
with open("list1m2020.csv", "r") as f:
    for line in f:

        #if table_exists:
        #    if debut <= ca_num.value:
        #        debut += 1
        #    else:
        #        table_exists = False

        #else:

        user = line.split()[0]
            #user_old = user
            #user, counter = get_url(user, counter)
            #if counter == cMax:
            #    ok = True
            #    ca_num += 1

        p = Process(target=processus, args=(user,))
        p.start()
        p.join()
            
        if (TIMEOUT.value != 5):
            TIMEOUT.value = 5

        
con.close()