import re

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
    def __init__(self, name, incipit, key, genre, year):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voice = []
        self.author = []


class Edition:
    def __init__(self, composition, name):
        self.composition = composition
        self.authors = []
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
        for i, k in enumerate(self.edition.composition.author):
            s += k.name
            if k.born is not None or k.died is not None:
                s += ' (' + to_str(k.born) + '--' + to_str(k.died) + ')'
            if i+1 != len(self.edition.composition.author):
                s += '; '
        dictionary['Composer'] = s
        dictionary['Title'] = self.edition.composition.name
        dictionary['Genre'] = self.edition.composition.genre
        dictionary['Key'] = self.edition.composition.key
        dictionary['Composition Year'] = str(self.edition.composition.year)
        dictionary['Edition'] = self.edition.name
        s = ''
        for i, k in enumerate(self.edition.authors):
            s += k.name
            if i+1 != len(self.edition.authors):
                s += ', '
        dictionary['Editor'] = s
        for i, k in enumerate(self.edition.composition.voice):
            dictionary['Voice ' + str(i+1)] = format_voice(k)
        if self.partiture:
            dictionary['Partiture'] = 'yes'
        else:
            dictionary['Partiture'] = 'no'
        dictionary['Incipit'] = self.edition.composition.incipit
        for k, v in dictionary.items():
            if v is not None and v != '' and v != '0':
                print(k + ': ' + str(v))

    def composition(self):
        return self.edition.composition


def load(filename):
    file = open(filename, 'r')
    entry = []
    prints = []
    for line in file:
        if line.strip() == '' and len(entry) > 1:
            prints.append(parse_entry(entry))
            entry = []
        else:
            entry.append(line)
    if len(entry) > 1:
        prints.append(parse_entry(entry))
    return prints


def to_str(i):
    if i is not None:
        return str(i)
    else:
        return ''


def parse_entry(entry):
    composition = Composition(None, None, None, None, 0)
    edition = Edition(composition, None)
    p = Print(edition, None, False)
    for line in entry:
        split = line.split(':')
        if len(split) < 2:
            continue
        split[1] = split[1].strip()
        if split[1] == '':
            continue
        if len(split) > 2:
            split[1] += ":" + split[2].strip()
            if len(split) > 3:
                split[1] += ":" + split[3].strip()
        if split[0] == 'Print Number':
            p.print_id = int(split[1])
        if split[0] == 'Composer':
            parse_person_composer(split[1], composition.author)
        if split[0] == 'Title':
            composition.name = split[1]
        if split[0] == 'Genre':
            composition.genre = split[1]
        if split[0] == 'Key':
            composition.key = split[1]
        if split[0] == 'Composition Year':
            regex = re.match(".*([1-2][0-9]{3})", split[1])
            if regex is not None:
                composition.year = int(regex.group(1))
        if split[0] == 'Edition':
            edition.name = split[1]
        if split[0] == 'Editor':
            parse_person_editor(split[1], edition.authors)
        if split[0].split(' ')[0] == 'Voice':
            composition.voice.append(parse_voice(split[1]))
        if split[0] == 'Partiture' and split[1] == 'yes':
            p.partiture = True
        if split[0] == 'Incipit':
            composition.incipit = split[1]
    return p


def parse_person_composer(line, l):
    split = line.split(';')
    for e in split:
        born = None
        died = None
        name = re.sub(r'\([^)]*\)', '', e).strip()
        regex = re.search(r'\((.*?)\)', e)
        if regex is not None:
            par = regex.group(1)
            plus_format = re.match(r'(^\+[0-9]{4})$', par)
            if plus_format is not None:
                died = int(plus_format.group(1))
            one_dash_format = re.match(r'^([0-9]{4})-([0-9]{4})$', par)
            if one_dash_format is not None:
                born = int(one_dash_format.group(1))
                died = int(one_dash_format.group(2))
            two_dash_format = re.match(r'^([0-9]{4})--([0-9]{4})$', par)
            if two_dash_format is not None:
                born = int(two_dash_format.group(1))
                died = int(two_dash_format.group(2))
            two_dash_born = re.match(r'^([0-9]{4})--$', par)
            if two_dash_born is not None:
                born = int(two_dash_born.group(1))
            two_dash_died = re.match(r'^--([0-9]{4})$', par)
            if two_dash_died is not None:
                died = int(two_dash_died.group(1))
            one_dash_born = re.match(r'^([0-9]{4})-$', par)
            if one_dash_born is not None:
                born = int(one_dash_born.group(1))
            one_dash_died = re.match(r'^-([0-9]{4})$', par)
            if one_dash_died is not None:
                died = int(one_dash_died.group(1))
        person = Person(name, born, died)
        l.append(person)


def parse_person_editor(line, l):
    split = line.split(',')
    s = ''
    for i, e in enumerate(split):
        e = e.strip()
        if more_than_one_word(e):
            if s != '':
                l.append(Person(s, None, None))
                s = ''
            l.append(Person(e, None, None))
        elif s != '':
            s += ', ' + e
            l.append(Person(s, None, None))
            s = ''
        else:
            s += e
            if len(split) == i+1:
                l.append(Person(e, None, None))


def more_than_one_word(s):
    x = s.strip()
    return len(x.split(' ')) > 1


def parse_voice(line):
    regex = re.match(r'^(\S+--\S+)(.*)', line.strip())
    rng = None
    if regex is not None:
        rng = regex.group(1).strip(',').strip(';')
        name = regex.group(2).strip()
        if name == '':
            name = None
    else:
        name = line
    return Voice(name, rng)


def format_voice(voice):
    s = ''
    if voice.range is not None:
        s += voice.range
        if voice.name is not None:
            s += ', '
    if voice.name is not None:
        s += voice.name
    return s
