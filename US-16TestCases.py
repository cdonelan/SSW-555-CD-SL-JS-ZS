import unittest

from getFamilyParser import genFamilyParser

class ParserTest(unittest.TestCase):

    def testPeopleIsntNone(self):
        personDic, familyDic = genFamilyParser()
        self.assertNotEqual(personDic, None)

    def testFamilyIsntNone(self):
        personDic, familyDic = genFamilyParser()
        self.assertNotEqual(familyDic, None)

    def testMalesHaveSameLastName(self):
        personDic, familyDic = genFamilyParser()
        firstMaleLastName = "Smith"
        for person in personDic.items():
            if person[1].get("Sex") != "F":
                self.assertEqual(person[1].get("Name").split('/')[1], firstMaleLastName)
        
    def testPeopleIsADictionary(self):
        personDic, familyDic = genFamilyParser()
        self.assertEqual(type(personDic) == dict, True)
    
    def testMalesHaveLastNames(self):
        personDic, familyDic = genFamilyParser()
        for person in personDic.items():
            if person[1].get("Sex") != "F":
                self.assertNotEqual(person[1].get("Name").split('/')[1], "")
        


    

if __name__ == "__main__":
    unittest.main()
