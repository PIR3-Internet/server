from re import L
import sqlite3
from cryptography.x509 import Extensions
import matplotlib.pyplot as plt
import numpy as np

con = sqlite3.connect('ca-providers.db')
cur = con.cursor()

#cur.execute("select * from ca")
#print(cur.fetchall())

#merge same providers together
cur.execute("UPDATE ca SET ca_provider='DigiCert Inc' WHERE ca_provider='DigiCert, Inc.'")
cur.execute("UPDATE ca SET ca_provider='Google Trust Services' WHERE ca_provider='Google Trust Services LLC'")
#beyond Google Trust Services, we merge all providers together
cur.execute("UPDATE ca SET ca_provider='Others' WHERE ca_provider NOT IN ('DigiCert Inc', 'Cloudflare, Inc.', \"Let's Encrypt\", 'Sectigo Limited', 'GlobalSign nv-sa', 'Amazon', 'GoDaddy.com, Inc.', 'Google Trust Services')")

##################                       CAMEMBERT                      ##################################

cur.execute("SELECT ca_provider, COUNT(*) provider_count FROM ca WHERE ca_provider IS NOT 'Others' GROUP BY ca_provider ORDER BY provider_count DESC")
#cur.execute("SELECT ca_provider, COUNT(*) provider_count FROM ca GROUP BY ca.ca_provider ORDER BY ca.ca_provider ASC")
# #print(cur.fetchall())
data = cur.fetchall()
print(data)
    
# Data to plot
ca_provider = []
provider_count = []
    
for row in data:
    ca_provider.append(row[0])
    provider_count.append(row[1])
    
cur.execute("SELECT ca_provider, COUNT(*) provider_count FROM ca WHERE ca_provider IS 'Others' GROUP BY ca_provider")
data = cur.fetchall()
print(data)
ca_provider.append(data[0][0])
provider_count.append(data[0][1])
    
#cur.execute("SELECT ca_provider FROM ca GROUP BY ca.ca_provider ORDER BY COUNT(*) DESC")
labels = ca_provider
#cur.execute("SELECT COUNT(*) provider_count FROM ca GROUP BY ca.ca_provider ORDER BY provider_count DESC")
sizes = provider_count  


########################                           CUMULATIVE FLOW DIAGRAM                           #########################

cur.execute("SELECT MAX(ca_num) FROM ca")
i_max = cur.fetchall()[0][0]
print(i_max)

scales = np.arange(0, i_max, 100)
scales = scales+99

DigiCert = []
Cloudflare = []
Let_s_Encrypt = []
Sectigo = []
GlobalSign = []
Amazon = []
GoDaddy = []
Google = []
Others = []

i=0
while (i < i_max):
#for i in scales:
    cur.execute("SELECT COUNT(*) provider_count FROM ca WHERE ca_provider IS 'DigiCert Inc' AND ca_num BETWEEN ? AND ? GROUP BY ca_provider", (i, i+99))
    data = cur.fetchall()
    if (DigiCert == []):
        DigiCert.append(data[0][0])
    elif (data == []):
        DigiCert.append(DigiCert[len(DigiCert) - 1])
    else:
        DigiCert.append(data[0][0] + DigiCert[len(DigiCert) - 1])

    
    cur.execute("SELECT COUNT(*) provider_count FROM ca WHERE ca_provider IS 'Cloudflare, Inc.' AND ca_num BETWEEN ? AND ? GROUP BY ca_provider", (i, i+99))
    data = cur.fetchall()
    if (Cloudflare == []):
        Cloudflare.append(data[0][0])
    elif (data == []):
        Cloudflare.append(Cloudflare[len(Cloudflare) - 1])
    else:
        Cloudflare.append(data[0][0] + Cloudflare[len(Cloudflare) - 1])
    
    cur.execute("SELECT COUNT(*) provider_count FROM ca WHERE ca_provider IS \"Let's Encrypt\" AND ca_num BETWEEN ? AND ? GROUP BY ca_provider", (i, i+99))
    data = cur.fetchall()
    if (Let_s_Encrypt == []):
        Let_s_Encrypt.append(data[0][0])
    elif (data == []):
        Let_s_Encrypt.append(Let_s_Encrypt[len(Let_s_Encrypt) - 1])
    else:
        Let_s_Encrypt.append(data[0][0] + Let_s_Encrypt[len(Let_s_Encrypt) - 1])

    
    cur.execute("SELECT COUNT(*) provider_count FROM ca WHERE ca_provider IS 'Sectigo Limited' AND ca_num BETWEEN ? AND ? GROUP BY ca_provider", (i, i+99))
    data = cur.fetchall()
    if (Sectigo == []):
        Sectigo.append(data[0][0])
    elif (data == []):
        Sectigo.append(Sectigo[len(Sectigo) - 1])
    else:
        Sectigo.append(data[0][0] + Sectigo[len(Sectigo) - 1])
    
    cur.execute("SELECT COUNT(*) provider_count FROM ca WHERE ca_provider IS 'GlobalSign nv-sa' AND ca_num BETWEEN ? AND ? GROUP BY ca_provider", (i, i+99))
    data = cur.fetchall()
    if (GlobalSign == []):
        GlobalSign.append(data[0][0])
    elif (data == []):
        GlobalSign.append(GlobalSign[len(GlobalSign) - 1])
    else:
        GlobalSign.append(data[0][0] + GlobalSign[len(GlobalSign) - 1])

    
    cur.execute("SELECT COUNT(*) provider_count FROM ca WHERE ca_provider IS 'Amazon' AND ca_num BETWEEN ? AND ? GROUP BY ca_provider", (i, i+99))
    data = cur.fetchall()
    if (Amazon == []):
        Amazon.append(data[0][0])
    elif (data == []):
        Amazon.append(Amazon[len(Amazon) - 1])
    else:
        Amazon.append(data[0][0] + Amazon[len(Amazon) - 1])
    
    cur.execute("SELECT COUNT(*) provider_count FROM ca WHERE ca_provider IS 'GoDaddy.com, Inc.' AND ca_num BETWEEN ? AND ? GROUP BY ca_provider", (i, i+99))
    data = cur.fetchall()
    if (GoDaddy == []):
        GoDaddy.append(data[0][0])
    elif (data == []):
        GoDaddy.append(GoDaddy[len(GoDaddy) - 1])
    else:
        GoDaddy.append(data[0][0] + GoDaddy[len(GoDaddy) - 1])

    
    cur.execute("SELECT COUNT(*) provider_count FROM ca WHERE ca_provider IS 'Google Trust Services' AND ca_num BETWEEN ? AND ? GROUP BY ca_provider", (i, i+99))
    data = cur.fetchall()
    if (Google == []):
        Google.append(data[0][0])
    elif (data == []):
        Google.append(Google[len(Google) - 1])
    else:
        Google.append(data[0][0] + Google[len(Google) - 1])

    
    cur.execute("SELECT COUNT(*) provider_count FROM ca WHERE ca_provider IS 'Others' AND ca_num BETWEEN ? AND ? GROUP BY ca_provider", (i, i+99))
    data = cur.fetchall()
    if (Others == []):
        Others.append(data[0][0])
    elif (data == []):
        Others.append(Others[len(Others) - 1])
    else:
        Others.append(data[0][0] + Others[len(Others) - 1])

    i += 100

providers_values = np.row_stack((DigiCert, Cloudflare, Let_s_Encrypt, Sectigo, GlobalSign, Amazon, GoDaddy, Google, Others))
providers = ['DigiCert Inc', 'Cloudflare, Inc.', 'Let\'s Encrypt', 'Sectigo Limited', 'GlobalSign nv-sa', 'Amazon', 'GoDaddy.com, Inc.', 'Google Trust Services', 'Others']


# Plot the pie chart 
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85)   #patches, texts = 
#plt.legend(patches, labels, loc="best")
plt.title('CA Providers for ' + str(i_max) + ' websites\n')
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.axis('equal')
plt.tight_layout()
plt.show()
plt.savefig("camemberts/"+str(i_max)+"camembert.png")


# plot the cumulative histogram
fig, ax = plt.subplots()
for val in range(len(providers)):
    ax.plot(scales, providers_values[val], linewidth=1.5, label=providers[val])
ax.grid(True)
ax.legend(loc='best')
ax.set_title('CA of ' + str(i_max) + ' websites')
ax.set_xlabel('Most visited websites')
ax.set_ylabel('Number of CA provided')
plt.show()
plt.savefig("CFD/CFD.png")


# plot the relative cumulative histogram
fig, ax = plt.subplots()
for val in range(len(providers)):
    ax.plot(scales, (providers_values/(scales))[val], linewidth=1.5, label=providers[val])
ax.grid(True)
ax.legend(loc='best')
ax.set_title('CA of ' + str(i_max) + ' websites')
ax.set_xlabel('Most visited websites')
ax.set_ylabel('Number of CA provided')
plt.show()
plt.savefig("CFD/CFD_relative.png")


#check results from table errors
print("")

cur.execute("SELECT COUNT(*) FROM errors")
nb_errors = cur.fetchall()[0][0]
print("Number of errors : ", nb_errors)

cur.execute("SELECT error, COUNT(*) error_count FROM errors GROUP BY error ORDER BY error_count DESC")
errors = cur.fetchall()
print(errors, "\n")

cur.execute("SELECT extension, COUNT(*) extension_count FROM errors GROUP BY extension ORDER BY extension_count DESC")
extensions = cur.fetchall()
print(extensions)

print("")

cur.execute("SELECT user FROM errors WHERE extension IS 'com' ORDER BY user ASC")
data = cur.fetchall()
print(data)

extension = []
extension_count = []
nb_others = 0
j = 0
for row in extensions:
    if j < 15:
        extension.append(row[0])
        extension_count.append(row[1])
    else:
        nb_others += row[1]
    j += 1
extension.append('Others')
extension_count.append(nb_others)

# Plot the pie chart for errors
fig, ax = plt.subplots()
plt.pie(extension_count, labels=extension, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
plt.title(str(nb_errors) + ' errors\n')
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.axis('equal')
plt.tight_layout()
plt.show()
plt.savefig("errors/errors.png")


con.close()