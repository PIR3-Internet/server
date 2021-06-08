import sqlite3
import matplotlib.pyplot as plt

con = sqlite3.connect('ca-providers.db')
cur = con.cursor()

#cur.execute("select * from ca")
#print(cur.fetchall())

#merge same providers together
cur.execute("UPDATE ca SET ca_provider='DigiCert Inc' WHERE ca_provider='DigiCert, Inc.'")
cur.execute("UPDATE ca SET ca_provider='Google Trust Services' WHERE ca_provider='Google Trust Services LLC'")
#beyond Google Trust Services, we merge all providers together
cur.execute("UPDATE ca SET ca_provider='Others' WHERE ca_provider NOT IN ('DigiCert Inc', 'Cloudflare, Inc.', \"Let's Encrypt\", 'Sectigo Limited', 'GlobalSign nv-sa', 'Amazon', 'GoDaddy.com, Inc.', 'Google Trust Services')")

cur.execute("SELECT ca_provider, COUNT(*) provider_count FROM ca WHERE ca_provider IS NOT 'Others' GROUP BY ca_provider ORDER BY provider_count DESC")
#cur.execute("SELECT ca_provider, COUNT(*) provider_count FROM ca GROUP BY ca.ca_provider ORDER BY ca.ca_provider ASC")
#print(cur.fetchall())
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
labels = ca_provider #labels =
#cur.execute("SELECT COUNT(*) provider_count FROM ca GROUP BY ca.ca_provider ORDER BY provider_count DESC")
sizes = provider_count #sizes = 
#colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
#explode = (0.1, 0, 0, 0)  # explode 1st slice

# Plot
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85)   #patches, texts = 
#plt.legend(patches, labels, loc="best")
plt.title('CA Providers\n')
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.axis('equal')
plt.tight_layout()
plt.show()
plt.savefig("camembert.png")

con.close()