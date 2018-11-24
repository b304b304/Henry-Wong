import ahocorasick
import _pickle as cPickle
from collections import defaultdict

entity_list_file = '/home/nico/Tasks/2018-2019_1/Week1/code/demo/search/data/all_entity.txt'
entity_out_path = '/home/nico/Tasks/2018-2019_1/Week1/code/demo/search/data/ent_ac.pkl'
attr_list_file = '/home/nico/Tasks/2018-2019_1/Week1/code/demo/search/data/attr_mapping.txt'
attr_out_path = '/home/nico/Tasks/2018-2019_1/Week1/code/demo/search/data/attr_ac.pkl'
val_list_file = '/home/nico/Tasks/2018-2019_1/Week1/code/demo/search/data/Person_val.txt'


def dump_ac_entity_dict(list_file, out_path):
    A = ahocorasick.Automaton()
    f = open(list_file)
    i = 0
    for line in f:
        word = line.strip()
        A.add_word(word.encode('utf-8'), (i, word.encode('utf-8')))
        i += 1
    A.make_automaton()
    with open(out_path, "wb") as attr:
        cPickle.dump(A, attr)
    f.close()


def dump_ac_attr_dict(attr_mapping_file, out_path):
    A = ahocorasick.Automaton()
    f = open(attr_mapping_file)
    i = 0
    for line in f:
        parts = line.strip().split(" ")
        for p in parts:
            if p != "":
                A.add_word(p, (i, p))
                i += 1
    A.make_automaton()
    return A
    cPickle.dump(A, open(out_path, 'wb'))


def load_ac_dict(out_path):
    A = cPickle.load(open(out_path, "rb"))
    return A


def load_attr_map(attr_mapping_file):
    f = open(attr_mapping_file)
    mapping = defaultdict(list)
    for line in f:
        parts = line.strip().split(" ")
        for p in parts:
            if p != '':
                mapping[p].append(parts[0])
    return mapping


def load_entity_dict(entity_file):
    f = open(entity_file)
    ents = {}
    for line in f:
        ents[line.strip()] = 1
    return ents


def load_val_dict(val_file):
    f = open(val_file)
    val_attr_map = dict()
    line_num = 0
    for line in f:
        parts = line.strip().split(" ")
        line_num += 1
        try:
            val_attr_map[parts[0]] = parts[1]
        except:
            val_attr_map[parts[0]] = "Null"
    return val_attr_map


if __name__ == '__main__':    
    dump_ac_attr_dict(attr_list_file, attr_out_path)
    load_val_dict(val_list_file)
    # load_val_dict("./search/data/Person_val.txt")