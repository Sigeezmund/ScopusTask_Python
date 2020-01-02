from googleDisk import getOurTeacher, putInfoInDB
from scopus.Person import Person, PersonFullInfo
from scopus.scopusRequest import getInfoAboutTeacher
from termcolor import colored

teacher = getOurTeacher()

fullInfo = []
i = 1
for oneTeacher in teacher:

    name = oneTeacher.name
    try:
        scopusInfo = getInfoAboutTeacher(oneTeacher)

        fullInfo.append(PersonFullInfo(oneTeacher, scopusInfo['document-count'],
                                       scopusInfo['cited-by-count'], scopusInfo['citation-count']))
        print("We Get Info About " + str(i) + " from " + str(len(teacher)))
        i = i + 1
    except TypeError as e:
        i = i + 1
        print(colored(e, 'red', attrs=['reverse', 'blink']))
        print(colored('Can\'t find info for: ' + name, 'red', attrs=['reverse', 'blink']))
putInfoInDB(fullInfo)
