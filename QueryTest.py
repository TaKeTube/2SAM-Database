from database import DataBase
import ASM
from schema import *
import Data

'''
TEST FILE FOR Q2(iii)
List all actors who never played in a movie suitable for small children.
PLEASE MAKE SURE YOU HAVE READ THE GRAMMAR FILE IF YOU WANT TO TEST MORE ABOUT THE QUERY.
'''

db = DataBase(list(relation_schema.keys()))
a = ASM.ASM(db)

# This is the data from the big database
# many tables and hard to check the correctness
Data.insertData(db)

# This is a small amount of data
# easy to check the correctness
# only yuan yue satisfied the requirement
'''
db.insert("RESTRICTION",("a",1984,"PG","USA"))
db.insert("RESTRICTION",("a",1984,"R18","JP"))
db.insert("RESTRICTION",("b",1988,"PG","USA"))
db.insert("RESTRICTION",("b",1988,"15","UK"))
db.insert("RESTRICTION",("c",1999,"PG","USA"))
db.insert("RESTRICTION",("c",1988,"R18","UK"))

db.insert("ROLE",(1,"a",1984,"friendA"))
db.insert("ROLE",(2,"a",1984,"mea"))
db.insert("ROLE",(1,"b",1988,"eee"))
db.insert("ROLE",(3,"b",1988,"yyyy"))
db.insert("ROLE",(3,"c",1999,"C#"))
db.insert("ROLE",(4,"c",1988,"py"))

db.insert("PERSON",(1,"Xie","Tian",1999))
db.insert("PERSON",(2,"Zhu","Zhongbo",1999))
db.insert("PERSON",(3,"Yuan","Yue",2001))
db.insert("PERSON",(4,"Zhang","Junkai",2000))
'''

# Notice:
#   If you want somthing to be a constant string, please add @ before it,
#   example1: @18 instead of 18, 
#             because 18 would be convert to float
#   example2: @RESTRICTION instead of RESTRICTION, 
#             because the latter one would be a list of entries and could not be used for searching using index structure

# A basic test for Q2
# Here R18 is not suitable for children
#a.Run("PERSON where (not (self.PERSON_id in ((((RESTRICTION where (self.RESTRICTION_description == R18)) cross ROLE) where ((self.RESTRICTION_title == self.ROLE_movie) and (self.RESTRICTION_year == self.ROLE_year))).ROLE_id)))")

# A test for searching using index structure
#a.Run("PERSON where (not (self.PERSON_id in ((((@RESTRICTION search {'RESTRICTION_description':'R18'}) cross ROLE) where ((self.RESTRICTION_title == self.ROLE_movie) and (self.RESTRICTION_year == self.ROLE_year))).ROLE_id)))")
#a.Run("(@RESTRICTION search {'RESTRICTION_description':'R18'}) cross ROLE")

# An almost complete test based on the restrictions
# Here R18, 18, R, IIB, K-16, MA is not suitable for children
# the basic test would using a long time (about 10 mins), so we need use the assignment function for the machine
#a.Run("PERSON where (not (self.PERSON_id in ((((RESTRICTION where ((self.RESTRICTION_description == R18) or (self.RESTRICTION_description == @18) or (self.RESTRICTION_description == R) or (self.RESTRICTION_description == IIB) or (self.RESTRICTION_description == K-16) or (self.RESTRICTION_description == MA))) cross ROLE) where ((self.RESTRICTION_title == self.ROLE_movie) and (self.RESTRICTION_year == self.ROLE_year))).ROLE_id)))")

# A test for assignment function
#a.Run("A = (((RESTRICTION where ((self.RESTRICTION_description == R18) or (self.RESTRICTION_description == @18) or (self.RESTRICTION_description == R) or (self.RESTRICTION_description == IIB) or (self.RESTRICTION_description == K-16) or (self.RESTRICTION_description == MA))) cross ROLE) where ((self.RESTRICTION_title == self.ROLE_movie) and (self.RESTRICTION_year == self.ROLE_year)))")
a.Run("B = (RESTRICTION where ((self.RESTRICTION_description == R18) or (self.RESTRICTION_description == @18) or (self.RESTRICTION_description == R) or (self.RESTRICTION_description == IIB) or (self.RESTRICTION_description == K-16) or (self.RESTRICTION_description == MA)))", 0)
a.Run("C = (B cross ROLE)", 0)
a.Run("A = (C where ((self.RESTRICTION_title == self.ROLE_movie) and (self.RESTRICTION_year == self.ROLE_year)))", 0)
#a.Run("A.ROLE_id")
actors = a.Run("PERSON where (not (self.PERSON_id in (A.ROLE_id)))")
print()
for i in actors:
    print(i[1]+' '+i[2])

# To check the roughly correction of the query, you could use code below
# the sum of numbers of entries in 2 table respectively should be the number of entries in PERSON table
print()
a.Run("count (PERSON where (not (self.PERSON_id in (A.ROLE_id))))")
a.Run("count (PERSON where (self.PERSON_id in (A.ROLE_id)))")
a.Run("count (PERSON)")

# testing code for test
#print(db.search_attributes("RESTRICTION",{'RESTRICTION_description':'R18'}))
#print(list(relation_schema.keys()))