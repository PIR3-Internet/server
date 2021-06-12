import sqlite3
import matplotlib.pyplot as plt
# import automatic_comp


def matching(name):
    name = name.upper()
    if "AMAZON" in name:
        return "AMAZON"
    if "ALIBABA" in name:
        return "ALIBABA"
    if "CHINA UNICOM" in name:
        return "CHINA UNICOM"
    if "CHINA TELECOM" in name:
        return "CHINA TELECOM"
    if "YAHOO" in name:
        return "YAHOO"
    if "HUAWEI" in name:
        return "HUAWEI"
    return name


def make_dico(conn, rank):
    org = {}
    corp = {}
    cursor = conn.execute('SELECT NS FROM DNS WHERE RANK<=?', rank)
    for url in cursor:
        if url not in org:
            org[url] = 1
        else:
            org[url] += 1
    for name in org.keys():
        corp_name = matching(name[0])
        if corp_name in corp.keys():
            corp[corp_name] += org[name]
        else:
            corp[corp_name] = org[name]
    return corp


def make_graph(dico, number):
    labels = []
    values = []
    i = 0
    for k, v in sorted(dico.items(), key=lambda x: x[1], reverse=True):
        i += 1
        if i < 10:
            labels.append((k, v))
            values.append(v)
        else:
            labels.append("")
            values.append(v)
    plt.pie(values, labels=labels, labeldistance=1.1)
    plt.gcf().set_size_inches(8,6)
    plt.title(f"Distribution for the {number} most popular domains")
    plt.show()


def modif_dico(dico, groups):
    new_dico = {'OTHERS':0}
    for name in dico.keys():
        if name not in groups:
            new_dico['OTHERS'] += dico[name]
        else:
            new_dico[name] = dico[name]
    return new_dico


def redondancy(conn, rank):
    cursor = conn.execute('SELECT COUNT(DISTINCT NS) FROM DNS WHERE RANK <=? GROUP BY URL', rank)
    multiple_NS = 0
    for numb in cursor:
        if numb>1:
            multiple_NS += 1
    return multiple_NS



if __name__ == "__main__":
    conn = sqlite3.connect('dns.db')

    redondancy_pourcentage = (redondancy(conn, 5000)/5000)*100

    dico100 = make_dico(conn, (100,))
    dico500 = make_dico(conn, (500,))
    dico1000 = make_dico(conn, (1000,))
    dico2000 = make_dico(conn, (2000,))
    dico3000 = make_dico(conn, (3000,))
    dico4000 = make_dico(conn, (4000,))
    dico5000 = make_dico(conn, (5000,))
    make_graph(dico500, 500)
    make_graph(dico5000, 5000)

    groups = [k for k, v in sorted(dico5000.items(), key=lambda x: x[1], reverse=True)]
    pop_groups = groups[:9]

    dico100 = modif_dico(dico100, pop_groups)
    dico500 = modif_dico(dico500, pop_groups)
    dico1000 = modif_dico(dico1000, pop_groups)
    dico2000 = modif_dico(dico2000, pop_groups)
    dico3000 = modif_dico(dico3000, pop_groups)
    dico4000 = modif_dico(dico4000, pop_groups)
    dico5000 = modif_dico(dico5000, pop_groups)

    pop_groups.append("OTHERS")
    pop_dico = {}
    for group in pop_groups:
        pop_dico[group] = [dico100[group]/100, dico500[group]/500, dico1000[group]/1000, dico2000[group]/2000, dico3000[group]/3000, dico4000[group]/4000, dico5000[group]/5000]
    print(pop_dico)

    fig, ax = plt.subplots()
    scales = [100, 500, 1000, 2000, 3000, 4000, 5000]
    for group in pop_dico.keys():
        ax.plot(scales, pop_dico[group], linewidth=1.5, label=group)

    ax.grid(True)
    ax.legend(loc = 'best', ncol = 2)
    ax.set_title('Most popular groups for NS')
    ax.set_xlabel('Most visited websites')
    ax.set_ylabel('Number of domains in NS operated within group')
    plt.show()



"""
    # Verfif AutoComp
    autocomp = automatic_comp.AutoComp(org=dico5000)
    autoTab = autocomp.comp()
    print(autoTab)
"""