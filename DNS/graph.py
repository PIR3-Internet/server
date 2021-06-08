import sqlite3
import matplotlib.pyplot as plt
import difflib


conn = sqlite3.connect('database.db')
c = conn.cursor()
org = {}

cursor = conn.execute('''SELECT NS FROM DNS''')
for url in cursor:
    if url not in org:
        org[url] = 1
    else:
        org[url]+=1

print(org)

"""
matching = []

for name in org.keys():
    isMatch = False
    for entry in matching:
        comp = difflib.SequenceMatcher(None, name[0], entry[0]).find_longest_match()
        print(comp)
        if comp.size > 4:
            entry.append(name)
            isMatch = True
            break
    if not isMatch:
        matching.append([name[0]])

print(matching)



labels = []
values = []
otherValue = 0
for k,v in sorted(org.items(), key=lambda x: x[1]):
    if v > 10:
        labels.append((k, v))
        values.append(v)
    else:
        labels.append("")
        values.append(v)
        # otherValue += v


# labels.append("Others")
# values.append(otherValue)

plt.pie(values, labels=labels)
plt.show()

"""