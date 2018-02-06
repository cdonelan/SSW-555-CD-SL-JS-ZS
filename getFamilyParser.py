#Shane Lynes, Zachary Shakked, Cassidy Donlean, and Jhustin Scarlett
#I pledge my honor that I have abided by the Stevens Honor System

import os

def genFamilyParser():
    infile = open('proj02test.ged', 'r')

    firstLevelTags = ['NOTE', 'HEAD', 'TRLR']
    firstLevelExceptions = ['INDI', 'FAM']
    secondLevelTags = ['NAME', 'SEX', 'BIRT', 'DEAT', 'MARR', 'DIV', 'FAMC', 'FAMS', 'HUSB', 'WIFE', 'CHIL']
    thirdLevelTags =['DATE']
    thirdLevelTagMonths = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    
    for line in infile:
        print(('--> ' + line).strip())
        if line[0] == '0':
            if checkIfValidTag(line, firstLevelTags) is True:
                ln = line.split()
                ln.append('Y')
            elif checkIfValidTagExc(line, firstLevelExceptions) is True:
                ln = line.split()
                ln = [ln[0], ln[2], ln[1], 'Y']
            else:
                ln = line.split()
                ln.append('N')
        elif line[0] == '1':
            if checkIfValidTag(line, secondLevelTags) is True:
                ln = line.split()
                ln.append('Y')
            else:
                ln = line.split()
                ln.append('N')
        elif line[0] == '2':
            if checkIfValidTagMonth(line, thirdLevelTags, thirdLevelTagMonths) is True:
                 ln = line.split()
                 ln.append('Y')
            else:
                ln = line.split()
                ln.append('N')
        else:
            ln = line.split()
            ln.append('N')
            
        outputString = '<-- ' + ln[0] + '|' + ln[1] + '|' + ln[-1] + '|'
        if len(ln) > 3:
            outputString = outputString + ln[2]
            for i in ln[3:-1]:
                outputString = outputString + ' ' + i #print all words in comment without  line between them
            
        print(outputString)


def checkIfValidTag(line, tags):
      parts = line.split()
      if parts[1] in tags:
          return True
      else:
          return False

def checkIfValidTagExc(line, tags):
    parts = line.split()
    if parts[2] in tags:
        return True
    else:
        return False

def checkIfValidTagMonth(line, tags, tags1):
    parts = line.split()
    if len(parts) == 5:
        if parts[1] in tags:
            if parts[3] in tags1:
                return True
            else:
                return False
        else:
            return False

genFamilyParser()
