
import re
import opcode
from opcode import *
import utils

def genomeSymbolsFromFile(filepath):
    genomeString = open(filepath, 'r').read()
    genomeString = re.sub(r"(\/\/.*\n)|(\/\/.*)| |\n", "", genomeString)
    return genomeString


def readSpawnTableFromFile(filepath):
    if filepath is None or filepath == "":
        return None
    
    spawnTableString = open(filepath, 'r').read()
    spawnTableString = re.sub(r"(\/\/.*\n)|(\/\/.*)", "", spawnTableString)
    
    spawnTable = [e.split('\t') for e in spawnTableString.split('\n')]
    spawnTable = [(int(e[1]), e[0],) for e in spawnTable]
    return spawnTable



