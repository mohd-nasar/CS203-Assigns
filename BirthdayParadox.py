import random

birthdateList = []
daysuntillbirthdaynotrepeated = []
no_of_trails = 1000

for _ in range(no_of_trails):
    while True:
        birthdate = random.randint(1, 365)
        if birthdate in birthdateList:
            daysuntillbirthdaynotrepeated.append(len(birthdateList))
            birthdateList.clear()
            break
        else:
            birthdateList.append(birthdate)
print(daysuntillbirthdaynotrepeated)
print(len(daysuntillbirthdaynotrepeated))