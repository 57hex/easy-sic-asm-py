optab = {
  "ADD": "18",
  "AND": "40",
  "COMP": "28",
  "DIV": "24",
  "J": "3C",
  "JEQ": "30",
  "JGT": "34",
  "JLT": "38",
  "JSUB": "48",
  "LDA": "00",
  "LDCH": "50",
  "LDL": "08",
  "LDX": "04",
  "MUL": "20",
  "OR": "44",
  "RD": "D8",
  "RSUB": "4C",
  "STA": "0C",
  "STCH": "54",
  "STL": "14",
  "STSW": "E8",
  "STX": "10",
  "SUB": "1C",
  "TD": "E0",
  "TIX": "2C",
  "WD": "DC"
}

inp = open('F2.txt', "r")
inter = open("interme.txt", "w")
symtab = open("symboltab.txt", "w")
sym = {}
head = ["Line \t", "Loc \t", "Source Statement \t"]
listToStr = '\t'.join([str(elem) for elem in head])
inter.write(listToStr)
inter.write('\n')
firstLine = inp.readline()
newL = firstLine.strip().split()
LOCCTR = 0
LINE = 5
if newL[1] == 'START':
  LOCCTR = newL[2]
  LOCCTR = hex(int(LOCCTR, 16))
start = LOCCTR
sl = []
sl = [str(LINE) + '\t\t', str(LOCCTR) + '\t\t\t', newL[0] + '\t', newL[1] + '\t', newL[2] + '\t']
listToStr = '\t'.join([str(elem) for elem in sl])
inter.write(listToStr)
inter.write('\n')
firstTime = True

for i in inp.readlines():
  n = i.strip().split()
  if n[0] != '.':
    if len(n) == 1:
      # objcode = optab[n[0]] + "0000"
      # write to inter
      LINE = LINE + 5
      sl = [str(LINE) + '\t', str(LOCCTR) + '\t', '\t', str(n[0])+ '\t']
      listToStr = '\t'.join([str(elem) for elem in sl])
      inter.write(listToStr)
      inter.write('\n')

      LOCCTR = hex(int(LOCCTR, 16) + (3))
    elif len(n) == 2:
      if n[0] != 'END':
        #write to inter
        LINE = LINE + 5
        sl = [str(LINE) + '\t', str(LOCCTR) + '\t', str(n[0]) + '\t', str(n[1])+ '\t']
        listToStr = '\t'.join([str(elem) for elem in sl])
        inter.write(listToStr)
        inter.write('\n')
        LOCCTR = hex(int(LOCCTR, 16) + (3))
      else:
        #write to inter
        LINE = LINE + 5
        sl = [str(LINE) + '\t', '\t' + '\t', str(n[0]) + '\t', str(n[1])+ '\t']
        listToStr = '\t'.join([str(elem) for elem in sl])
        inter.write(listToStr)
        inter.write('\n')

        #write to sym
        sl = [n[0], LOCCTR]
        listToStr = '\t'.join([str(elem) for elem in sl])
        symtab.write(listToStr)
        symtab.write('\n')

    else :
      
      if n[0] not in optab.keys() and (n[1] != "WORD" and n[1] != "RESW" and n[1] != "RESB" and n[1] != "BYTE"):
        #write to symtab
        sl = [n[0], LOCCTR]
        listToStr = '\t'.join([str(elem) for elem in sl])
        symtab.write(listToStr)
        symtab.write('\n')

        #write to intern
        LINE = LINE + 5
        sl = [str(LINE) + '\t', str(LOCCTR) + '\t', str(n[0]) + '\t', str(n[1])+ '\t', str(n[2])+ '\t']
        listToStr = '\t'.join([str(elem) for elem in sl])
        inter.write(listToStr)
        inter.write('\n')

        LOCCTR = hex(int(LOCCTR, 16) + (3))

      elif n[1] in optab.keys() or n[1] == "WORD":
        if (n[1] == "WORD"):
          count = format(int(n[2]), '04x')
          # objcode = '00' + str(count)
          # write to itern
          LINE = LINE + 5
          sl = [str(LINE) + '\t', str(LOCCTR) + '\t', str(n[0]) + '\t', str(n[1])+ '\t', str(n[2])+ '\t']
          listToStr = '\t'.join([str(elem) for elem in sl])
          inter.write(listToStr)
          inter.write('\n')

          # write to symb
          sl = [n[0], LOCCTR]
          listToStr = '\t'.join([str(elem) for elem in sl])
          symtab.write(listToStr)
          symtab.write('\n')

          LOCCTR = hex(int(LOCCTR, 16) + (3))
        elif (n[1] != "WORD"):

          # write to intern
          LINE = LINE + 5
          sl = [str(LINE) + '\t', str(LOCCTR) + '\t', str(n[0]) + '\t', str(n[1])+ '\t', str(n[2])+ '\t']
          listToStr = '\t'.join([str(elem) for elem in sl])
          inter.write(listToStr)
          inter.write('\n')

          # write to symb
          sl = [n[0], LOCCTR]
          listToStr = '\t'.join([str(elem) for elem in sl])
          symtab.write(listToStr)
          symtab.write('\n')

          LOCCTR = hex(int(LOCCTR, 16) + (3))
      elif n[1] == "RESW":
        # write to intern
        LINE = LINE + 5
        sl = [str(LINE) + '\t', str(LOCCTR) + '\t', str(n[0]) + '\t', str(n[1])+ '\t', str(n[2])+ '\t']
        listToStr = '\t'.join([str(elem) for elem in sl])
        inter.write(listToStr)
        inter.write('\n')
        temp = int(n[2], 16)

        # write to symb
        sl = [n[0], LOCCTR]
        listToStr = '\t'.join([str(elem) for elem in sl])
        symtab.write(listToStr)
        symtab.write('\n')

        LOCCTR = hex(int(LOCCTR, 16) + (temp) * 3)
      elif n[1] == "RESB":
        #write to intern
        LINE = LINE + 5
        sl = [str(LINE) + '\t', str(LOCCTR) + '\t', str(n[0]) + '\t', str(n[1])+ '\t', str(n[2])+ '\t']
        listToStr = '\t'.join([str(elem) for elem in sl])
        inter.write(listToStr)
        inter.write('\n')

        #write to symb
        sl = [n[0], LOCCTR]
        listToStr = '\t'.join([str(elem) for elem in sl])
        symtab.write(listToStr)
        symtab.write('\n')

        LOCCTR = hex(int(LOCCTR, 16) + int(n[2]))
      elif n[1] == "BYTE":
        if n[2][0] == "X":
          #write to intern
          LINE = LINE + 5
          sl = [str(LINE) + '\t', str(LOCCTR) + '\t', str(n[0]) + '\t', str(n[1])+ '\t', str(n[2])+ '\t']
          listToStr = '\t'.join([str(elem) for elem in sl])
          inter.write(listToStr)
          inter.write('\n')

          #write to symb
          sl = [n[0], LOCCTR]
          listToStr = '\t'.join([str(elem) for elem in sl])
          symtab.write(listToStr)
          symtab.write('\n')
          LOCCTR = hex(int(int(LOCCTR,16)+(len(n[2])-3)/2))
        elif n[2][0] == "C":
          #write to intern
          LINE = LINE + 5
          sl = [str(LINE) + '\t', str(LOCCTR) + '\t', str(n[0]) + '\t', str(n[1])+ '\t', str(n[2])+ '\t']
          listToStr = '\t'.join([str(elem) for elem in sl])
          inter.write(listToStr)
          inter.write('\n')

          #write to symb
          sl = [n[0], LOCCTR]
          listToStr = '\t'.join([str(elem) for elem in sl])
          symtab.write(listToStr)
          symtab.write('\n')
          LOCCTR = hex(int(LOCCTR, 16) + (len(n[2])-(3)))
      
inp.close()
symtab.close()
inter.close()