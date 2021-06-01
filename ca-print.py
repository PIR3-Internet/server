import sqlite3
import matplotlib.pyplot as plt

con = sqlite3.connect('ca-providers.db')
cur = con.cursor()

#cur.execute("select * from ca")
#print(cur.fetchall())

cur.execute("SELECT ca_provider, COUNT(*) provider_count FROM ca GROUP BY ca.ca_provider ORDER BY provider_count DESC")
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

#cur.execute("SELECT ca_provider FROM ca GROUP BY ca.ca_provider ORDER BY COUNT(*) DESC")
labels = ca_provider #labels =
#cur.execute("SELECT COUNT(*) provider_count FROM ca GROUP BY ca.ca_provider ORDER BY provider_count DESC")
sizes = provider_count #sizes = 
#colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
#explode = (0.1, 0, 0, 0)  # explode 1st slice

# Plot
patches, texts = plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
plt.legend(patches, labels, loc="best")

plt.axis('equal')
plt.show()
plt.savefig("camembert.png")

con.close()