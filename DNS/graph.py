import sqlite3
import matplotlib.pyplot as plt
import difflib


def matching(name):
    if "AMAZON" in name:
        return "Amazon"
    if "Alibaba" in name:
        return "Alibaba"
    if "CHINANET" in name:
        return "ChinaNet"
    if "Chinanet" in name:
        return "ChinaNet"
    if "CHINA UNICOM" in name:
        return "China Unicom"
    if "China Unicom" in name:
        return "China Unicom"
    if "YAHOO" in name:
        return "Yahoo"
    if "Huawei" in name:
        return "Huawei"
    return name


def make_graph(dico):
    labels = []
    values = []
    for k, v in sorted(dico.items(), key=lambda x: x[1]):
        if v > 10:
            labels.append((k, v))
            values.append(v)
        else:
            labels.append("")
            values.append(v)
    plt.pie(values, labels=labels)
    plt.show()

if __name__ == "__main__":

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    org = {}

    cursor = conn.execute('''SELECT NS FROM DNS''')
    for url in cursor:
        if url not in org:
            org[url] = 1
        else:
            org[url] += 1

    print(org)

    corp = {}

    for name in org.keys():
        corp_name = matching(name[0])
        print(corp_name)
        if corp_name in corp.keys():
            corp[corp_name] += org[name]
        else:
            corp[corp_name] = org[name]

    print(corp)
    make_graph(org)
    make_graph(corp)






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