from pass1 import optab, LOCCTR, start, sym
import re
symtab = open("symboltab.txt", "r")
objpgm = open("objpgm.txt", "w")
finalpgm = open("final.txt", "w")
intere = open("interme.txt", "r")
address = format(int(start, 16), '06x')
T = ["T",str(address)]
Tcount = 0

def addLen(objcode, case, address, statement="", argument=0):
  global T
  global Tcount
  length = len(''.join([str(elem) for elem in T]))
  if case == "END":
    count = hex(Tcount)
    realCount = format(int(str(count), 16), '02x')
    T.insert(2, realCount)
    Tstring = ''.join([str(elem) for elem in T])
    objpgm.write(Tstring)
    objpgm.write('\r')
    return

  if length+6 > 67:
    count = hex(Tcount)
    realCount = format(int(str(count), 16), '02x')
    T.insert(2, realCount)
    Tstring = ''.join([str(elem) for elem in T])
    objpgm.write(Tstring)
    objpgm.write('\r')
    address = format(int(address, 16), '06x')
    T = ["T",str(address)]
    T.append(objcode)
    Tcount = 3
  elif case == 1:
    Tcount += 3
    T.append(objcode)
  elif case == 2:
    Tcount += 3
    T.append(objcode)
  elif case == 3:
    if statement == "BYTE":
      if argument[0] == "X":
        Tcount += 1
        T.append(objcode)
      elif argument[0] == "C" :
        Tcount += 3
        T.append(objcode)
    elif statement == "RESB":
      # Tcount += 3
      T.append("      ")
    elif statement == "RESW":
      # Tcount += 3
      T.append("      ")
    elif statement == "WORD":
      Tcount += 3
      T.append(objcode)
    else:
      Tcount += 3
      T.append(objcode)

for j in symtab.readlines():
  n = j.strip().split()
  address = format(int(n[1], 16), '04x')
  sym.update({n[0]: address})
  
for i in intere.readlines():
  ls = i.strip().split()
  if ls[0] != "Line" :
    if len(ls) == 3:
      if ls[1] != "END":
        opcode = str(optab[ls[2]]) + "0000"
        ls.append(opcode)
        listToStr = '\t'.join([str(elem) for elem in ls])
        finalpgm.write(listToStr)
        finalpgm.write('\n')
        addLen(opcode, 1, ls[2])
      elif ls[1] == "END":
        listToStr = '\t'.join([str(elem) for elem in ls])
        finalpgm.write(listToStr)
        finalpgm.write('\n')
        address = format(int(sym["FIRST"],16), '06x')
        objText = "E" + str(address)
        addLen("", "END", "")
        objpgm.write(objText)
        objpgm.write('\n')

    elif len(ls) == 4:
      if ls[2] == "LDCH" or ls[2] == "STCH" or ls[2] == "LDA" or ls[2] == "STA" or ls[2] == "LDX" or ls[2] == "STX" or ls[2] == "LDL" or ls[2] == "STL": 
        key = ls[3].split(',')
        if len(key) == 2:
          opcode = str(optab[ls[2]])
          address = int(sym[key[0]],16)
          flag = 0x8000
          realAddress = hex(address+flag)
          address = format(int(realAddress, 16), '04x')

          opcode = opcode + str(address)
          ls.append(opcode)
          listToStr = '\t'.join([str(elem) for elem in ls])
          finalpgm.write(listToStr)
          finalpgm.write('\n')
          addLen(opcode, 2, ls[1])
        else:
          opcode = str(optab[ls[2]])  + str(sym[ls[3]])
          ls.append(opcode)
          listToStr = '\t'.join([str(elem) for elem in ls])
          finalpgm.write(listToStr)
          finalpgm.write('\n')
          addLen(opcode, 2, ls[1])

      elif ls[0] != "Line" and ls[2] != "LDCH" and ls[2] != "STCH":
        opcode = str(optab[ls[2]]) + str(sym[ls[3]])
        ls.append(opcode)
        listToStr = '\t'.join([str(elem) for elem in ls])
        finalpgm.write(listToStr)
        finalpgm.write('\n')
        addLen(opcode, 2, ls[1])

      
    elif len(ls) == 5 and ls[3] != "START":
      if ls[2] not in optab.keys() and (ls[3] != "WORD" and ls[3] != "RESW" and ls[3] != "RESB" and ls[3] != "BYTE"):
        opcode = str(optab[ls[3]]) + str(sym[ls[4]])
        ls.append(opcode)
        listToStr = '\t'.join([str(elem) for elem in ls])
        finalpgm.write(listToStr)
        finalpgm.write('\n')
        addLen(opcode, 3, ls[1], ls[3], ls[4])
      elif ls[3] == "WORD":
        opcode = "00"
        address = format(int(ls[4], 16), '04x')
        opcode = opcode + str(address)
        ls.append(opcode)
        listToStr = '\t'.join([str(elem) for elem in ls])
        finalpgm.write(listToStr)
        finalpgm.write('\n')
        addLen(opcode, 3,ls[1], ls[3], ls[4])
      elif ls[3] == "BYTE":
        key = ls[4].split("'")
        if key[1] in sym.keys() and key[1] != "EOF":
          opcode = str(sym[key[1]])
          ls.append(opcode)
          listToStr = '\t'.join([str(elem) for elem in ls])
          finalpgm.write(listToStr)
          finalpgm.write('\n')
          addLen(opcode, 3, ls[1], ls[3], ls[4])
        elif key[0] == "C":
          charToAscii = [ord(c) for c in key[1]]
          opcode = ''.join(format(x, '02x') for x in charToAscii)
          ls.append(opcode)
          listToStr = '\t'.join([str(elem) for elem in ls])
          finalpgm.write(listToStr)
          finalpgm.write('\n')
          addLen(opcode, 3, ls[1], ls[3], ls[4])
        else:
          opcode = str(key[1])
          ls.append(opcode)
          listToStr = '\t'.join([str(elem) for elem in ls])
          finalpgm.write(listToStr)
          finalpgm.write('\n')
          addLen(opcode, 3, ls[1], ls[3], ls[4])
      else:
        listToStr = '\t'.join([str(elem) for elem in ls])
        finalpgm.write(listToStr)
        finalpgm.write('\n')
        addLen(opcode, 3, ls[1], ls[3], ls[4])

    elif ls[3] == "START":
      listToStr = '\t'.join([str(elem) for elem in ls])
      finalpgm.write(listToStr)
      finalpgm.write('\n')
      headAddress = format(int(ls[1], 16), '06x')
      dispAddress = hex(int(sym["END"], 16) - int(ls[1],16))
      realAddress = format(int(dispAddress, 16), '06x')
      objText = "H" + str(ls[2]) + '\t' + headAddress + realAddress
      objpgm.write(objText)
      objpgm.write('\n')

