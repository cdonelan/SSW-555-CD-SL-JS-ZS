def divorceBeforeDeath (familyDic, personDic):
    divorces = {}
    for key, family in familyDic.items():
        husbandID = family["Husband ID"]
        wifeID = family["Wife ID"]
        if "Divorced" not in famimly:
            continue
        if not isPersonAlive(husbandID, personDic):
            continue
        if not isPersonAlive(wifeID, personDic):
            continue

        if wifeID in divorces:
            print('Family ID is: ' + key)
            print('Wife ID is: ' + wifeID + ' ' + personDic[wifeID]['Name'])
            if isPersonAlive(wifeID, personDic):
                print("US06: This wife has been divorced before death")
            divorces[wifeID] += 1
        else:
            marriages[wifeID] = 1

        if husbandID in divorces:
            print('Family ID is: ' + key)
            print('Husband ID is: ' + husbandID + ' ' + personDic[husbandID])
            if isPersonAlive(husbandID, personDic):
                print("US06: This husband has been divorced before death")
            divorces[husbandID] += 1
        else:
            marriages[husbandID] = 1


def marriageAfterFourteen(familyDic, personDic):
    for key,family in familyDic.items():
        husbandID = family["Husband ID"]
        wifeID = family["Wife ID"]
        if "Divorced" in family:
            continue
        if getIndividualAge(personDic[husbandID], dic)> 14:
            continue
        if getIndividualAge(personDic[wifeID], dic) > 14:
            continue

        print('Family ID is: ' + key)
        print('Wife ID is: ' + wifeID + ' ' + personDic[wifeID]['Name'])
        print('Husband ID is:' + husbandID + ' ' + personDic[husbandID]['Name'])

        if int(getIndividualAge(personDic[wifeID], dic)) < 14:
                print("US10: This wife has been married before 14")
    
        if int(getIndividualAge(personDic[husbandID], dic)) < 14:
                print("US10: This husband has been married before 14")

