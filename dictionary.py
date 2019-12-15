import json

class Character:
    def __init__(self, e, d, t):
        self.is_end = e
        self.dictionary = d
        self.type = t

def getWords():
    words = {}
    f = open('arrays.json', 'r')
    json_raw = f.read()
    array = json.loads(json_raw)

    print('Started parsing words')

    for w in array:
        prev = words
        for i, c in enumerate(w):
            if c == '|':
                t = 0
                if w[i+1:] == "ot":
                    t = 1
                elif w[i+1:] == "sf":
                    t = 2
                elif w[i+1:] == "ol":
                    t = 3
                elif w[i+1:] == "rv":
                    t = 4
                elif w[i+1:] == "fl":
                    t = 5
                elif w[i+1:] == "sn":
                    t = 6

                prev.is_end = True
                prev.type = t
                break
            else:
                if prev.get(c) == None:
                    prev[c] = Character(False, {}, 0)
                if i < len(w) - 4:
                    prev = prev[c].dictionary
                else:
                    prev = prev[c]
    print('Done parsing words')
    return words

words = getWords()
print('Enter word:')
w = input()

result = ''