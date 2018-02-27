#I pledge my honor that I have abided by the Stevens Honor System
#Shane Lynes

import unittest

from getFamilyParser_withoutBadSmells import genFamilyParser

class ParserTest(unittest.TestCase):

    #tests that the individual keys from the parser are correct, and nothing was duplicated
    def testArePeopleKeysEqual(self):
        personDic, familyDic = genFamilyParser()
        rightList = ['I01','I02','I03','I04','I05','I06','I07','I08','I09','I10','I11','I12','I13','I14']
        functionList = list()
        for i in personDic.keys():
            functionList.append(i)

        self.assertListEqual(sorted(functionList), rightList)

    #tests that the family keys from the parser are correct, and nothing was duplicated
    def testAreFamKeysEqual(self):
        personDic, familyDic = genFamilyParser()
        rightList = ['F01','F02','F03','F04','F05']
        functionList = list()
        for i in familyDic.keys():
            functionList.append(i)

        self.assertListEqual(sorted(functionList), rightList)

    #tests that the first individual name matches up with the parser, to ensure it was overwritten by duplicate
    def testPersonNotOverWritten(self):
        personDic, familyDic = genFamilyParser()
        correctFirstPerson = 'Shane /Smith/ '

        self.assertEqual(correctFirstPerson, personDic['I01']['Name'])

    #tests that the first family husband name matches up with the parser, to ensure it was overwritten by duplicate
    def testFamilyNotOverWritten(self):
        personDic, familyDic = genFamilyParser()
        correctFirstFamilyHusbandName = 'John /Smith/ '

        self.assertEqual(correctFirstFamilyHusbandName, familyDic['F01']['Husband Name'])
    
    #tests that all Family keys are unique in returned results
    def testAllFamKeysNotEqual(self):
        personDic, familyDic = genFamilyParser()
        functionList = list()
        for i in familyDic.keys():
            functionList.append(i)

        self.assertTrue(len(functionList) == len(set(functionList)))

    #tests that all individual keys are unique in returned results
    def testAllIndKeysNotEqual(self):
        personDic, familyDic = genFamilyParser()
        functionList = list()
        for i in personDic.keys():
            functionList.append(i)

        self.assertTrue(len(functionList) == len(set(functionList)))

    

    
if __name__ == "__main__":
    unittest.main()
