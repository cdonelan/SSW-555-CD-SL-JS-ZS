import unittest

from getFamilyParser import genFamilyParser

class ParserTest(unittest.TestCase):

    def testArePeopleKeysEqual(self):
        personDic, familyDic = genFamilyParser()
        rightList = ['I01','I02','I03','I04','I05','I06','I07','I08','I09','I10','I11','I12','I13','I14']
        functionList = list()
        for i in personDic.keys():
            functionList.append(i)

        self.assertListEqual(sorted(functionList), rightList)

    def testAreFamKeysEqual(self):
        personDic, familyDic = genFamilyParser()
        rightList = ['F01','F02','F03','F04','F05']
        functionList = list()
        for i in familyDic.keys():
            functionList.append(i)

        self.assertListEqual(sorted(functionList), rightList)

    

if __name__ == "__main__":
    unittest.main()
