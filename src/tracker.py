from sim import SimulationData
import os, os.path

from const import *

class Tracker:
    _logs = []
    MAX_LOG_SIZE_BEFORE_WRITE = 100
    BODY_OPENER = '`'
    BODY_CLOSER = '`'
    FOLDER_PATH = './runLogs/'
    
    
    def __init__(self, data):
        # below line modified from https://stackoverflow.com/a/2632251
        self.filenum = len([name for name in os.listdir(self.FOLDER_PATH)])
        self.filename = self.FOLDER_PATH + "run" + str(self.filenum) + ".txt"

        f = open(self.filename, "w+")
        f.write("log of run number " + str(self.filenum) + "\n")
        f.write('filename "' + str(self.filename) + '"\n')
        f.write("body opener = \"" + self.BODY_OPENER + "\"" + "\n")
        f.write("body closer = \"" + self.BODY_CLOSER + "\"" + "\n")
        
        # RECORD OPCODES IN ORDER, LISTING THEIR NUMERICAL CONVERSIONS
        # RECORD ALL CONSTANTS
        
        f.write("SYMBOL META DATA\n\n")
        import pprint
        printer = pprint.PrettyPrinter(indent=4, stream=f)
        
        f.write("Spawn Table:\n")
        printer.pprint(data.spawnTable)
        f.write("\n\n")
        
        f.write("Symbol Dictionary:\n")
        printer.pprint(data.opcodes._SYMBOL_DICTIONARY)
        f.write("\n\n")
        
        f.write("INITIAL SOUP\n")
        f.write(self.encode(data) + "\n")
        f.close()
        
    
    def lineBreak(self, simString, lineLen=80):
        return '\n'.join([''.join(simString[i:i+lineLen]) for i in range(0, len(simString), lineLen)])
    
    
    def encode(self, data):
        retval = ""
        retval += self.lineBreak([block["header"]["symbol"] for block in data.blocks])
        retval += "\n\nBODIES:"
        
        for i in range(len(data.blocks)):
            block = data.blocks[i]
            if block["header"]["type"] != "instruction":
                retval += "\n" + self.encodeBlock(i, block)
        return retval
    
    
    def encodeBlock(self, addr, block):
        retval = str(addr) + "\t" + block["header"]["symbol"]
        if block["header"]["type"] != "instruction":
            retval += self.BODY_OPENER + str(block["body"]) + self.BODY_CLOSER
        return retval
    
    
    def log(self, data):
        self._logs.append("\n\t")
        self._logs.append("cycle " + str(data.cycle))
        
        for addr in data._blockBodyUpdates:
            self._logs.append(self.encodeBlock(addr, data.blocks[addr]) + "\tBODY")
        for addr in data._blockUpdates:
            self._logs.append(self.encodeBlock(addr, data.blocks[addr]) + "\tBLOCK")
        if len(data._mutationLocations) > 0:
            self._logs.append("MUTATIONS @ " + str(data._mutationLocations))
         
        if len(self._logs) >= self.MAX_LOG_SIZE_BEFORE_WRITE:
            self._writeLogs()
        
        
    def _writeLogs(self):
        f = open(self.filename, "a")
        f.write('\n'.join(self._logs) + "\n")
        f.close()
        self._logs.clear()
        
