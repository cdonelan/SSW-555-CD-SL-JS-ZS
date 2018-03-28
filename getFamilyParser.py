#Shane Lynes, Zachary Shakked, Cassidy Donlean, and Jhustin Scarlett
#I pledge my honor that I have abided by the Stevens Honor System

import os
import datetime
import unittest
from prettytable import PrettyTable

def genFamilyParser():
    infile = open('My-Family-23-Jan-2018-602.ged', 'r')

    print('Sprint 1:\n')
    personDic = {}
    familyDic = {}

    firstLevelTags = ['NOTE', 'HEAD', 'TRLR']
    firstLevelExceptions = ['INDI', 'FAM']
    secondLevelTags = ['NAME', 'SEX', 'BIRT', 'DEAT', 'MARR', 'DIV', 'FAMC', 'FAMS', 'HUSB', 'WIFE', 'CHIL']
    thirdLevelTags =['DATE']
    thirdLevelTagMonths = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    individualDic = {'NAME': 'Name', 'SEX': 'Sex', 'FAMC': 'Child', 'FAMS': 'Spouse'}
    importantDateDic = {'BIRT': 'Birthday', 'DEAT': 'Death', 'MARR': 'Marriage', 'DIV': 'Divorce'}
    parentDic = {'HUSB': ['Husband ID', 'Husband Name'], 'WIFE': ['Wife ID', 'Wife Name']} #defines the parent structure
    datesDic = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT' : '10', 'NOV' : '11', 'DEC' : '12'} #can make date in proper format with #
    
    currentID = ""
    currentDic = {}
    dateType = ''
    duplicateCheck = 0
    for line in infile:
        if line[0] == '0':
            duplicateCheck = 0
            if checkIfValidTagExc(line, firstLevelExceptions) is True:
                ln = line.split()
                if ln[2] == 'INDI':
                    if checkIfKeyInDictionaryExists(ln[1].replace("@", ""),personDic): #if key already in person dictionary
                        print('US22: duplicate individual found, 1st one being taken')
                        print('User being taken: ' + currentID + ' ' + personDic[currentID]['Name'])
                        duplicateCheck = 1
                        continue #go to next iteration and do not include
                    currentID = ln[1].replace("@", "") #this replaces the"@" that was seen in the ID's of the GEDCOM file
                    personDic[currentID] = {'Name': '', 'Sex': '', 'Birthday': '', 'Age': '', 'Death': 'N/A', 'Alive': 'True', 'Spouse': 'N/A', 'Child': 'N/A'} #initializes our dictionaries
                    currentDic = personDic #we are now editing the individual dictionary
                elif ln[2] == 'FAM':
                    if checkIfKeyInDictionaryExists(ln[1].replace("@", ""),familyDic): #if key already in family dictionary
                        print('US 22: duplicate family found, 1st one being taken')
                        print('Family being taken: ' + currentID + ' Husband ID: ' + familyDic[currentID]['Husband Name'])
                        duplicateCheck = 1
                        continue #go to next iteration and do not include
                    currentID = ln[1].replace("@", "")
                    familyDic[currentID] = {'Marriage': '', 'Husband Name': '', 'Husband Name': '', 'Wife ID': '', 'Wife Name': '','Children': [], 'Divorce': 'N/A'}  #initializes our dictionaries
                    currentDic = familyDic #we are now editing the family dictionary
        elif line[0] == '1' and duplicateCheck != 1:
            if checkIfValidTag(line, secondLevelTags) is True:
               ln = line.split()
               if ln[1] in importantDateDic.keys():
                   dateType = importantDateDic[ln[1]] #get date type such as marriage, death, or birth
                   if dateType == 'Death':
                       personDic[currentID]['Alive'] = 'False' #if Death than make alive false in dic
               elif ln[1] in individualDic.keys():
                   tag = individualDic[ln[1]]
                   if ln[1] == 'NAME':
                       value = ''
                       for i in ln[2:]:
                           value += i + ' '
                       personDic[currentID][tag] = value[0:] #allows us to get the full name (including the last name)
                   else:
                       value = ln[2]
                       personDic[currentID][tag] = value.replace("@", "")
               else:
                   if ln[1] in parentDic.keys():
                       tags = parentDic[ln[1]]
                       familyDic[currentID][tags[0]] = ln[2].replace("@", "")
                       familyDic[currentID][tags[1]] = personDic[ln[2].replace("@", "")]['Name'] #put parents in the family dictionary
                   else:
                       familyDic[currentID]['Children'].append(ln[2].replace("@", "")) #put children in the family dictionary
        elif line[0] == '2' and duplicateCheck != 1:
            if checkIfValidTagMonth(line, thirdLevelTags, thirdLevelTagMonths) is True:
                 ln = line.split()
                 currentDic[currentID][dateType] = ln[4] + '-' + datesDic[ln[3]] + '-' + ln[2] #make date in the proper format as shown in the example on canvas
                 if currentDic == personDic:
                     personDic[currentID]['Age'] = getIndividualAge(currentID, personDic) #if we are in the person dictionary than give that person an age
                     
                 testDate = datetime.datetime.strptime(currentDic[currentID][dateType], '%Y-%m-%d').date()
                 checkIfValidDate(currentID, currentDic, testDate)  
                    
    peopleTable = PrettyTable(["ID", 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse'])

    personDic = checkUniqueNameBirthday(personDic)
    checkMalesNamesAreSame(personDic, familyDic)
    checkForPolygamy(familyDic, personDic)
    checkForMarriageBeforeDivorceOrDeath(familyDic, personDic)
    print('\nSprint 2:\n')
    checkForAge(personDic)
    checkForCorrespondingEntries(personDic, familyDic)
    checkNoMoreThanFiveSiblingsBornAtSameTime(personDic, familyDic)
    checkParentsDontMarryDescendants(personDic, familyDic)
    marriageAfterFourteen(personDic, familyDic)
    divorceBeforeDeath(personDic, familyDic)
    print('\nSprint3:\n')
    listLivingMarried(personDic, familyDic)
    listLivingSingle(personDic)
    checkCorrectGender(personDic, familyDic)
    checkAuntsAndUncles(personDic, familyDic)

    for key,val in sorted(personDic.items()):
        row = list([key, val['Name'], val['Sex'], val['Birthday'], val['Age'], val['Alive'], val['Death'], val['Child'], val['Spouse']])
        peopleTable.add_row(row)
    print('\nIndividuals')
    print(peopleTable)

    familyTable = PrettyTable(["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"])

    for key,val in sorted(familyDic.items()):
        row = list([key, val['Marriage'], val['Divorce'], val['Husband ID'], val['Husband Name'], val['Wife ID'], val['Wife Name'], val['Children']])
        familyTable.add_row(row)
    print('Families')
    print(familyTable)

    return personDic, familyDic

def getIndividualAge(personID, dic):
    currentDate = datetime.date.today()
    birthday = list(dic[personID]['Birthday'].split('-'))
    birthdayDate = datetime.date(int(birthday[0]), int(birthday[1]), int(birthday[2]))
    days = 0
    if dic[personID]['Alive'] == 'False':
        death = list(dic[personID]['Death'].split('-'))
        deathDate = datetime.date(int(death[0]), int(death[1]), int(death[2]))

    if dic[personID]['Alive'] == 'True': 
        days = (currentDate - birthdayDate).days
        years = days/365
    else:
        days = (deathDate - birthdayDate).days
        years = days/365
        
    checkIfValidAge(personID, dic, int(years))
    
    return str(int(years))

def checkIfValidTag(line, tags):
      parts = line.split()
      if parts[1] in tags:
          return True
      else:
          return False

def checkIfValidTagExc(line, tags):
    parts = line.split()
    if len(parts) == 3:
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

def checkUniqueNameBirthday(personDic):
    names = []
    birthdays = []
    excluded = []
    values = {}
    checker = 0
    for key,value in sorted(personDic.items()):
        if value['Birthday'] not in birthdays and value['Name'] not in names:
            names.append(value['Name'])
            birthdays.append(value['Birthday'])
            values[key] = value
        if value['Name'] in names and value['Birthday'] not in birthdays:
            names.append(value['Name'])
            birthdays.append(value['Birthday'])
            values[key] = value
        else:
            excluded.append(key)
            checker += 1
    if checker > 1:
        print('US 23: duplicate names and birthday found, this being is being excluded')
        for i in excluded:
            if i not in values.keys():
                print('Person being excluded: ' + i + ' ' + personDic[i]['Name'])
    return values

def checkMalesNamesAreSame(personDic, familyDic):
    for key,family in familyDic.items():
        father = getPerson(family["Husband ID"], personDic)
        fathersLastName = getLastName(father)
        children = getChildren(family, personDic)
        for child in children:
            if child["Sex"] == "M" and getLastName(child) != fathersLastName:
                print('US 16: Male child does not have same last name as father, check the table below.')
                print('Male child is: ' + child['Name'])

def checkForPolygamy(familyDic, personDic):
    marriages = {}
    for key,family in familyDic.items():
        husbandID = family["Husband ID"]
        wifeID = family["Wife ID"]
        if "Divorced" in family:
            continue
        if not isPersonAlive(husbandID, personDic):
            continue
        if not isPersonAlive(wifeID, personDic):
            continue
        
        if wifeID in marriages:
            print('Wife ID in marriages twice without divorce or death')
            print('Family ID is: ' + key)
            print('Wife ID is: ' + wifeID + ' ' + personDic[wifeID]['Name'])
            marriages[wifeID] += 1
        else:
            marriages[wifeID] = 1

        if husbandID in marriages:
            print('Husband ID in marriages twice without divorce or death')
            print('Family ID is: ' + key)
            print('Husband ID is: ' + husbandID + ' ' + personDic[husbandID])
            marriages[husbandID] += 1
        else:
            marriages[husbandID] = 1
             
    for key, count in marriages.items():
      if count > 1:
        print('US11: Polygamy has occurred for person mentioned above. This includes either marriage happening before divorce, or marriage happening before a spouse death. Check the family table.')



def checkForMarriageBeforeDivorceOrDeath(familyDic, personDic):
    marriages = {}
    for key,family in familyDic.items():
        husbandID = family["Husband ID"]
        wifeID = family["Wife ID"]
        if "Divorced" in family:
            continue
        if not isPersonAlive(husbandID, personDic):
            continue
        if not isPersonAlive(wifeID, personDic):
            continue
        
        if wifeID in marriages:
            print('Family ID is: ' + key)
            print('Wife ID is: ' + wifeID + ' ' + personDic[wifeID]['Name'])
            if isPersonAlive(wifeID, personDic):
                print("US05: This wife has been married again before death")
            if "Divorced" not in family:
                print("US06: This wife has been married again before divorce")
            marriages[wifeID] += 1
        else:
            marriages[wifeID] = 1

        if husbandID in marriages:
            print('Family ID is: ' + key)
            print('Husband ID is: ' + husbandID + ' ' + personDic[husbandID])
            if isPersonAlive(husbandID, personDic):
                print("US05: This husband has been married again before death")
            if "Divorced" not in family:
                print("US06: This husband has been married again before divorce")
            marriages[husbandID] += 1
        else:
            marriages[husbandID] = 1


# better smell, instead of duplicating if code, made a function
def checkIfKeyInDictionaryExists(line, dict):
    if line in dict.keys():
        return True
    else:
        return False

def getPerson(id, personDic):
    person = personDic[id]
    person["ID"] = id
    return person

def getLastName(person):
    return person.get("Name").split('/')[1]
    
def getChildren(family, personDic):
    childrenIDs = family.get("Children")
    children = []
    for childrenID in childrenIDs:
        children.append(getPerson(childrenID, personDic))
    return children

def isPersonAlive(personID, personDic):
  if getPerson(personID, personDic)["Alive"] == "True":
      return True
  else:
      return False

def checkIfValidDate(personID, dic, testDate):
    currentDate = datetime.date.today()
    if currentDate < testDate:
        print('US01: Person found with birthday past todays date, as shown in table below.')
        print('Person is: ' + personID + ' ' + dic[personID]['Name'])
        
def checkIfValidAge(personID, dic, age):
    if age > 150:
        print('US07: Person detected with an age of over 150 years, as shown in table below.')
        print('Person is: ' + personID + ' ' + dic[personID]['Name'])


def checkForAge(personDic):
    counter = 0
    for key,value in personDic.items():
        if value['Age'] !=  "":
            counter += 1
        else:
            print("US27: Not all ages were reported. Error for this individual: " + key + " " + value['Name'])

    if counter == len(personDic):
        print("US27: All individuals have an age reported as shown in the table below. Otherwise error would be reported.")

def checkForCorrespondingEntries(personDic, familyDic):
    childCountSuccess = 0
    childCounter = 0
    familyCounter = 0
    familyCountSuccess = 0
    for key,value in personDic.items():
        if value['Child'] != 'N/A':
            childCounter += 1
            familyID = value['Child']
            if key in familyDic[familyID]['Children']:
                childCountSuccess += 1
            else:
                print("US26: Child not in family--> Child ID: " + key + " FamilyID: " + familyID)

        if value['Spouse'] != 'N/A':
            familyCounter += 1
            familyID = value['Spouse']
            if familyDic[familyID]['Husband ID'] == key or familyDic[familyID]['Wife ID'] == key:
                familyCountSuccess += 1
            else:
                print("US26: Spouse not in family----> SpouseID: " + key + " FamilyID: " + familyID)

    if childCountSuccess == childCounter:
        print("US26: All children have a corresponding family entry.")
    if familyCountSuccess == familyCounter:
        print("US26: All spouses have a corresponding family entry.")
        
    husbandChecker = True
    wifeChecker = True
    indChecker =  True
    for key,value in familyDic.items():
        if value['Children'] != 'N/A':
            for i in value['Children']:
                if i not in personDic.keys():
                    indChecker == False
                    print("US26: Family child not in individual table--> Child ID: " + i + " FamilyID: " + key)
        if value['Wife ID'] not in personDic.keys():
            wifeChecker == False
            print("US26: Wife not in indiviudal table-----> Wife ID: " + value['Wife ID'] + " FamilyID: " + key)
        if value['Husband ID'] not in personDic.keys():
            husbandChecker == False
            print("US26: Wife not in indiviudal table-----> Husband ID: " + value['Husband ID'] + " FamilyID: " + key)

    if husbandChecker == True:
        print("US26: All husband family entries have a individual record entry.")
    if wifeChecker == True:
        print("US26: All wife family entries have a individual record entry.")
    if indChecker == True:
        print("US26: All children family entries have a individual record entry.")

# US-14 No more than five siblings should be born at the same time
def checkNoMoreThanFiveSiblingsBornAtSameTime(personDic, familyDic):
    for key, family in familyDic.items():
        children = getChildren(family, personDic)
        if children.count < 5:
            continue
        birthdays = {}
        for child in children:
            birthday = child["Birthday"]
            if birthday not in birthdays.keys():
                birthdays[birthday] = 1
            else:
                birthdays[birthday] = birthdays[birthday] + 1
        if len(birthdays) > 0:
            for key1, birthdaysCount in birthdays.items():
                if birthdaysCount > 5:
                    print("US14: Family with ID: " + key + " had more than 5 children at once.")
                else:
                    print("US14: No more than five siblings are born at the same time---> Family ID: " + key)

# US-17 Parents should not marry any of their descendants
def checkParentsDontMarryDescendants(personDic, familyDic):
    wifeCounter  = 0
    husbandCounter = 0
    for key, family in familyDic.items():
        # Get descendants
        children = getChildren(family, personDic)
        husbandID = family["Husband ID"]
        wifeID = family["Wife ID"]
        for child in children:
            childID = child["ID"]
            childsMarriage = getMarriage(child["ID"], familyDic)
            if childsMarriage != None:
                partnersID = getPartnersID(childID, childsMarriage)
                if husbandID in partnersID:
                    husbandCounter += 1
                    print("US17: Child with ID:" + childID + " married Dad with ID: " + husbandID)
                if wifeID in partnersID:
                    wifeCounter += 1
                    print("US17: Child with ID:" + childID + " married Mom with ID: " + wifeID)

    if husbandCounter == 0:
        print("US17: Husband did not marry any of their descendants")
    if wifeCounter == 0:
        print("US17: Wife did not marry any descendants")
                
        
            
def getMarriage(personID, familyDic):
    for key, family, in familyDic.items():
            if family["Husband ID"] == personID or family["Wife ID"] == personID:
                return family
    return None

def getPartnersID(personID, family):
    if family["Husband ID"] == personID:
        return family["Wife ID"]
    return family["Husband ID"]


# US-06 Divorce can only occur before death of both spouses
def divorceBeforeDeath(personDic, familyDic):
    counter = 0
    for key, family in familyDic.items():
        husbandID = family["Husband ID"]
        wifeID = family["Wife ID"]
        if (family['Divorce'] != 'N/A' and personDic[husbandID]['Death'] != 'N/A') or (family['Divorce'] != 'N/A' and personDic[wifeID]['Death'] != 'N/A'):
            divorce = list(family['Divorce'].split('-'))
            divorceDate = datetime.date(int(divorce[0]), int(divorce[1]), int(divorce[2]))
            divDays = 0
            currentDate = datetime.date.today()
            divDays = (currentDate - divorceDate).days
            divorceYears = divDays/365
            wifeDeathYears = 0
            husbandDeathYears = 0
            if personDic[husbandID]['Death'] != 'N/A':
                husbandDeathYears = int(getIndividualAge(husbandID, personDic))
            if personDic[wifeID]['Death'] != 'N/A':
                wifeDeathYears = int(getIndividualAge(wifeID, personDic))
            if husbandDeathYears > divorceYears:
                counter += 1
                print("US06: Divorce occured before death of husband: " + key + " Spouse ID: " + family['Husband ID']) 
            if wifeDeathYears > divorceYears:
                counter += 1
                print("US06: Divorce occured before death of wife: " + key + " Spouse ID: " + family['Wife ID'])

    if counter == 0:
        print("US06: All divorces occured before death.")


# US-10 Parents must be at least 14 years old            
def marriageAfterFourteen(personDic, familyDic):
    for key,family in familyDic.items():
        husbandID = family["Husband ID"]
        wifeID = family["Wife ID"]
        if "Divorced" in family:
            continue

        if int(getIndividualAge(wifeID, personDic)) <= 14:
            print('Family ID is: ' + key)
            print('Wife ID is: ' + wifeID + ' ' + personDic[wifeID]['Name'])
            print("US10: This wife has been married before 14")
                
        elif int(getIndividualAge(husbandID, personDic)) <= 14:
            print('Family ID is: ' + key)
            print('Husband ID is: ' + husbandID + ' ' + personDic[husbandID]['Name'])
            print("US10: This husband has been married before 14")
                                                                                                        

# US-30 List living married
def listLivingMarried(personDic, familyDic):
    print("US-30: People who are married and living are listed below:\n")
    for key,family in familyDic.items():
        if family["Divorce"] == 'N/A':
            husbandID = family["Husband ID"]
            wifeID = family["Wife ID"]
            if personDic[husbandID]["Alive"] == "True":
                print("Person ID: " + husbandID + " Person Name: " + personDic[husbandID]["Name"])
            if personDic[wifeID]["Alive"] == "True":
                print("Person ID: " + wifeID + " Person Name: " + personDic[wifeID]["Name"])

# US-31 List living single above 30
def listLivingSingle(personDic):
    print("\nUS31: People who are single, living, and above 30 are listed below:\n")
    for key,person in personDic.items():
        if person["Spouse"] == 'N/A' and int(person["Age"]) > 30 and person["Alive"] == "True":
                print("Person ID: " + key + " Person Name: " + person["Name"] + " Person Age: " + person["Age"])

def getAuntAndUncle (person, personDic, familyDic):
    AuntsUncles = []
    for key, family in familyDic.items():
        husbandID = family["Husband ID"]
        wifeID = family["Wife ID"]
        if person["ID"] in family.get("Children"):
            for parentID in [husbandID, wifeID]:
                for key, parentFamily in familyDic.items():
                    if parentID in parentFamily.get("Children"):
                        for child in getChildren(parentFamily, personDic):
                            if child["ID"] != parentID:
                                AuntsUncles.append(child["ID"])
    return AuntsUncles
                
            
# US-20 Aunts and uncles should not marry their nieces or nephews
def checkAuntsAndUncles(personDic, familyDic):
    for key, family in familyDic.items():
        # Get descendants
        children = getChildren(family, personDic)
        husbandID = family["Husband ID"]
        wifeID = family["Wife ID"]
        for child in children:
            childID = child["ID"]
            childsMarriage = getMarriage(child["ID"], familyDic)
            if childsMarriage != None:
                partnersID = getPartnersID(childID, childsMarriage)
                if partnersID in getAuntAndUncle(child, personDic, familyDic):
                    print ("\nUS20: " + childID + " cannot marry " + partnersID + "because aunts and uncles cannot marry nieces and nephews")
            
# US-21 Husband in family should be male and wife in family should be female
def checkCorrectGender(personDic, familyDic):
    for key,family in familyDic.items():
        husbandID = family["Husband ID"]
        wifeID = family["Wife ID"]

        father = getPerson(family["Husband ID"], personDic)
        wife = getPerson(family["Wife ID"], personDic)

        if father["Sex"] == "F":
            print('\nFamily ID is: ' + key)
            print ('Husband ID is: ' + husbandID + ' ' + personDic[husbandID]['Name'])
            print('US 21: Gender role of ' + husbandID + ' does not match')
            
        elif wife["Sex"] == "M":
            print('\nFamily ID is: ' + key)
            print ('Wife ID is: ' + wifeID + ' ' + personDic[wifeID]['Name'])
            print('US 21: Gender role of ' + wifeID + ' does not match')            
        
genFamilyParser()
