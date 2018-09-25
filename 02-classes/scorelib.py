class Person:
    def __init__(self, name, born, died):
        self.name = name
        self.born = born
        self.died = died


class Voice:
    def __init__(self, name, range):
        self.name = name
        self.range = range


class Composition:
    def __init__(self, name, incipit, key, genre, year, voice, author):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voice = voice
        self.author = author


class Edition:
    def __init__(self, composition, authors, name):
        self.composition = composition
        self.authors = authors
        self.name = name


class Print:
    def __init__(self, edition, print_id, partiture):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def format(self):
        dictionary = {}
        dictionary['Print Number'] = self.print_id
        s = ''
        for i,k in enumerate(self.edition.composition.author):
            s += k.name
            if (k.born is not None and k.died is not None):
                s += '(' + str(born) + '-' + str(died) + ')'
            if (i+1 != len(self.edition.composition.author)):
                s += '; '
        dictionary['Composer'] = s
        dictionary['Title'] = self.edition.composition.name
        dictionary['Genre'] = self.edition.composition.genre
        dictionary['Key'] = self.edition.composition.key
        dictionary['Composition Year'] = str(self.edition.composition.year)
        dictionary['Edition'] = self.edition.name
        s = ''
        for i,k in enumerate(self.edition.authors):
            s += k.name
            if (i+1 != len(self.edition.authors)):
                s += '; '
        dictionary['Editor'] = s
        for i,k in enumerate(self.edition.composition.voice):
            dictionary['Voice ' + str(i+1)] = k
        if self.partiture:
            dictionary['Partiture'] = 'no'
        else:
            dictionary['Partiture'] = 'yes'
        dictionary['Incipit'] = self.edition.composition.incipit
        for k,v in dictionary:
            print(k + ': ' + v)

    def composition(self):
        return self.edition.composition

def load(filename):
    l = [];
