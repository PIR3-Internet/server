import sqlite3
import difflib


class AutoComp():
    def __init__(self, org):
        self.org = org

    def comp(self):
        matching = []

        for name in self.org.keys():
            isMatch = False
            for entry in matching:
                comp = difflib.SequenceMatcher(None, name[0], entry[0]).ratio()
                if comp > 0.6:
                    entry.append(name)
                    isMatch = True
                    break
            if not isMatch:
                matching.append([name[0]])

        return matching
