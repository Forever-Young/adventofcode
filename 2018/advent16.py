from aocd import get_data
from dataclasses import dataclass, field
from typing import List
from collections import defaultdict


@dataclass
class Sample:
    before: List = field(default_factory=list)
    instr: List = field(default_factory=list)
    after: List = field(default_factory=list)
    behaves_like: List = field(default_factory=list)
    

class Solver16:
    def __init__(self, inp):
        self.samples = []
        self.test = []
        self.mapping = defaultdict(list)
        it = iter(inp.split('\n'))
        
        while True:
            try:
                line = next(it)
                if not line:
                    break  # next would be test program
                before = list(map(int, line[9:-1].split(', ')))
                line = next(it)
                instr = list(map(int, line.split(' ')))
                line = next(it)
                after = list(map(int, line[9:-1].split(', ')))
                self.samples.append(Sample(before=before, instr=instr, after=after))
                next(it)  # skip blank line
            except StopIteration:
                break
                
        while True:
            try:
                line = next(it)
                if not line:
                    continue
                instr = list(map(int, line.split(' ')))
                self.test.append(instr)
            except StopIteration:
                break
            
    def execute(self, opcode, instr, regs):
        if opcode is None and instr[0] in self.mapping and len(self.mapping[instr[0]]) == 1:
            opcode = self.mapping[instr[0]][0]   
        if opcode is None:
            raise Exception(f'{instr[0]} ambiguous')

        if opcode == 'addr' or opcode == 0:
            regs[instr[3]] = regs[instr[1]] + regs[instr[2]]
        if opcode == 'addi' or opcode == 1:
            regs[instr[3]] = regs[instr[1]] + instr[2]
        if opcode == 'mulr' or opcode == 2:
            regs[instr[3]] = regs[instr[1]] * regs[instr[2]]
        if opcode == 'muli' or opcode == 3:
            regs[instr[3]] = regs[instr[1]] * instr[2]
        if opcode == 'banr' or opcode == 4:
            regs[instr[3]] = regs[instr[1]] & regs[instr[2]]
        if opcode == 'bani' or opcode == 5:
            regs[instr[3]] = regs[instr[1]] & instr[2]
        if opcode == 'borr' or opcode == 6:
            regs[instr[3]] = regs[instr[1]] | regs[instr[2]]
        if opcode == 'bori' or opcode == 7:
            regs[instr[3]] = regs[instr[1]] | instr[2]
        if opcode == 'setr' or opcode == 8:
            regs[instr[3]] = regs[instr[1]]
        if opcode == 'seti' or opcode == 9:
            regs[instr[3]] = instr[1]
        if opcode == 'gtir' or opcode == 10:
            regs[instr[3]] = 1 if instr[1] > regs[instr[2]] else 0
        if opcode == 'gtri' or opcode == 11:
            regs[instr[3]] = 1 if regs[instr[1]] > instr[2] else 0
        if opcode == 'gtrr' or opcode == 12:
            regs[instr[3]] = 1 if regs[instr[1]] > regs[instr[2]] else 0
        if opcode == 'eqir' or opcode == 13:
            regs[instr[3]] = 1 if instr[1] == regs[instr[2]] else 0
        if opcode == 'eqri' or opcode == 14:
            regs[instr[3]] = 1 if regs[instr[1]] == instr[2] else 0
        if opcode == 'eqrr' or opcode == 15:
            regs[instr[3]] = 1 if regs[instr[1]] == regs[instr[2]] else 0
        
    def solve(self):
        for sample in self.samples:
            for opcode in range(16):
                regs = sample.before[:]
                self.execute(opcode, sample.instr, regs)
                if sample.after == regs:
                    if opcode not in self.mapping[sample.instr[0]]:
                        self.mapping[sample.instr[0]].append(opcode)
                    sample.behaves_like.append(opcode)
        
        return sum([1 for x in self.samples if len(x.behaves_like) >= 3])
    
    def eliminate_dups(self):
        while True:
            changed = False
            
            to_remove = []
            not_touch = []
            for op, maps in self.mapping.items():
                if len(maps) == 1:
                    to_remove.append(maps[0])
                    not_touch.append(op)
                    
            for remove in to_remove:
                for op, maps in self.mapping.items():
                    if remove in maps and op not in not_touch:
                        maps.remove(remove)
                        changed = True
            
            if not changed:
                break
    
    def solve2(self):
        self.solve()
        self.eliminate_dups()

        regs = [0] * 4
        for test in self.test:
            self.execute(None, test, regs)
        
        return regs[0]
        

solver = Solver16(get_data(day=16, year=2018))
print(solver.solve())
print(solver.solve2())

