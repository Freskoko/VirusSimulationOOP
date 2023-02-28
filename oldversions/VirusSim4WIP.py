import random
import matplotlib.pyplot as plt
import string
from collections import Counter

letters = string.ascii_lowercase

#TODO ADD POPULATION GROWTH, AND MAKE MUTATIONS MORE REAL, 
#TODO VIRUSES DONT HAVE SAME PROPERTIES JUST SAME NAMES, GIVER THEM PROTPERITES WHEN U MAKE THEM IT WILL SAVE
#A PROPERTIES DICT( MAKE OWN FUNCTION TO MAKER THAT)
#TODO CLEANN UP CODE ITS TOO MESSY


#initial conditions
NUM_PEOPLE = 50000
SICKATDAYZERO = 10
SIMULATION_DAYS = 70
MUTATION_CHANCE = 1 # in 100
PEOPLE_BORN_PERCENT = 1 #fix line 42
LOCKDOWN_REQUIREMENT = 100 #percent
LOCKDOWN_TAKEAWAY = 0 #percent

def RemoveDup(listobj):
    return list(dict.fromkeys(listobj))

def CreateRandomString():
    return( ''.join(random.choice(letters) for i in range(10)) ) 

def CreateRandomVirusVariables():
    returndict = {
        "incubation_period" : random.randint(2,4),
        "lethality" : 1,
        "infectivity": random.randint(3,10)         #random.randint(1,virus.infectivity) 
    }
    return returndict

class Virus:
    def __init__(self,name,inputdict):

        #from dict
        self.stringid = name
        self.incubation_period = inputdict.get("incubation_period")
        self.infectivity = inputdict.get("infectivity")  #random.randint(1,virus.infectivity) 

        #not from dict
        self.daysInPerson = 0
 

    def printDays(self):
        return f"days in person = {self.daysInPerson}"

    def returnID(self):
        return str(self.stringid)

    def ReturnData(self):
        return f"{self.__dict__.items()}"
       

class PersonInstance:
    def __init__(self):

        self.currentInfections = []
        self.Immunties = []
        self.immune_response_days = random.randint(5,6) 
        self.friends=random.randint(2,4)
        self.dead = False

        #---
        #WIP
        self.death_chance = 1

    def AddInfection(self,infection):
        newlist = []

        for vir in self.currentInfections: #this fixed everything
            newlist.append(vir.returnID())

        if infection.returnID() not in newlist:
            self.currentInfections.append(infection)   
    
    def RemoveInfection(self,infection):
        if infection in self.currentInfections:
            self.currentInfections.remove(infection)

    def addImmunity(self,infection):
        if infection not in self.Immunties:
            self.Immunties.append(infection)

    def Kill(self):
        if self.dead == False:
            self.dead = True

    def printInfections(self):
        for i in self.currentInfections:
            print(i.returnID())
        

def StartSimulation():
    PeopleList = []
    
    for i in range(NUM_PEOPLE):
        PeopleList.append(PersonInstance())

    NewVirusVar = CreateRandomVirusVariables()
    Name = "FirstVirus"

    for i in range(SICKATDAYZERO):

        NewVirus = Virus(Name,NewVirusVar)

        PeopleList[i].AddInfection(NewVirus)

    returndict = {}
    returndict.setdefault("PeopleList",PeopleList)
            
    return returndict

def RunOneDay(inputdict):
    
    PeopleList = inputdict.get("PeopleList")

    sickcounter = 0
    deathcounter = 0
    lockdown = True

    #population growth (relative to current pop)
    for i in range(round(  (PEOPLE_BORN_PERCENT/1000)*len(PeopleList)  )):
        PeopleList.append(PersonInstance())

    #iterate over people and interactions happen

    for person in PeopleList:

        if len(person.currentInfections) > 0 and person.dead == False:

            sickcounter+=1
            
            for viralinfection in person.currentInfections:
            
                #mutation
                if random.randint(1,30000000) == 1:

                    NewVirusVar = CreateRandomVirusVariables()
                    Name = CreateRandomString()

                    NewVirus = Virus(Name,NewVirusVar)

                    person.AddInfection(NewVirus)
                    
                    for i in range(10):

                        NewVirus = Virus(Name,NewVirusVar)

                        Friend = random.choice(PeopleList)
                        if viralinfection not in Friend.Immunties and viralinfection not in Friend.currentInfections:
                            
                            Friend.AddInfection(NewVirus) #tada
                #-------------------------------------------

                #increment days

                viralinfection.daysInPerson = viralinfection.daysInPerson + 1

                #die or live
                if viralinfection.daysInPerson >= person.immune_response_days:
                            
                    # if person.death_chance <= viralinfection.lethality: #die
                    if person.death_chance == random.randint(1,50):
                        try:
                            # PeopleList.remove(person)
                            deathcounter+=1
                            person.Kill()

                        except Exception as e:
                            pass
                        
                    else: #alive

                        person.addImmunity(viralinfection)
                        person.RemoveInfection(viralinfection)

                #incubation period
                if viralinfection.daysInPerson >= viralinfection.incubation_period:

                    #infect people
                    for _ in range(0,random.randint(0,person.friends)):

                        Friend = random.choice(PeopleList)
                    
                        if viralinfection not in Friend.Immunties and viralinfection not in Friend.currentInfections and Friend.dead == False:
                            
                            #chance to infect 
                            if random.randint(1,3) == 1:

                                NewVirusVar = CreateRandomVirusVariables()
                                Name = CreateRandomString()

                                NewVirus = Virus(Name,NewVirusVar)

                                Friend.AddInfection(NewVirus) #tada

    returndict = {}

    returndict.setdefault("PeopleList",PeopleList)
    returndict.setdefault("deathcounter",deathcounter)
    returndict.setdefault("sickcounter",sickcounter)
    returndict.setdefault("lockdown",lockdown)

    if inputdict.get("currentday") == None:
        returndict.setdefault("currentday",0)
    else:
        returndict.setdefault("currentday",inputdict.get("currentday")+1)

    return returndict

def runSimulation(days):

    SickPPLperday = []
    deadPPLperday = []
    lockdownlist = []
    virusdatadict = {}

    datadict = RunOneDay(StartSimulation())

    for i in range(days):

        datadict = RunOneDay(datadict)
        day = datadict.get("currentday")

        print(f" DAY {day} of {days} COMPLETED",sep=' ', end='\n', flush=True)

        SickPPLperday.append(datadict.get("sickcounter"))
        deadPPLperday.append(datadict.get("deathcounter"))
        lockdownlist.append(datadict.get("lockdown"))

        #get data from person list and count which infections!

        PeopleList = datadict.get("PeopleList")

        LargeList_OfInfections = []

        for person in PeopleList:
            for infection in person.currentInfections:
                if len(person.currentInfections) > 10:
                    print(len(person.currentInfections))
                if person.dead == False:
                    g = infection.returnID()
                    LargeList_OfInfections.append(g)

        print(len(LargeList_OfInfections)) #ok so a lot of infections getting addded here 

        cnt = Counter()
        
        for word in LargeList_OfInfections:
            cnt[word] += 1

        #something wrong with how infections are counted 
        for virusName,virusCount in cnt.items():
            if virusName in virusdatadict:

                virusCountAndDayTup = (day,virusCount)
                
                virusdatadict[virusName].append(virusCountAndDayTup)

            if virusName not in virusdatadict:
                virusCountAndDayTup = (day,virusCount)
                virusdatadict.setdefault(virusName,[virusCountAndDayTup])

    returndict = {}

    returndict.setdefault("virusdatadict",virusdatadict)
    returndict.setdefault("SickPPLperday",SickPPLperday)
    returndict.setdefault("deadPPLperday",deadPPLperday)
    returndict.setdefault("lockdownlist",lockdownlist)

    # print(cnt)
    
    return returndict

def PlotData(inputdict):

    print("Plotting Started")

    virusdatadict = inputdict.get("virusdatadict")

    # print(virusdatadict)

    for key,val in virusdatadict.items():
        xs = [x for x, y in val]
        ys = [y for x, y in val]           
        plt.plot(xs,ys)

    plt.plot(inputdict.get("SickPPLperday"), "om")

    plt.plot(inputdict.get("deadPPLperday"), "r--") #red
    # plt.plot(inputdict.get("lockdownlist"))

    death = inputdict.get("deadPPLperday")

    plt.suptitle(f"Virus simulation")
    plt.title(f"Conditions: {NUM_PEOPLE} people | {SICKATDAYZERO} sick at day 1 | total dead:{sum(death)} | {(sum(death)/NUM_PEOPLE)*100}%",fontsize=10)
    plt.xlabel("Days since first infection")
    plt.ylabel("Amount of people infected")
    plt.savefig("images/virusfigWIP8")

    print("Plotting Complete")
    plt.show()
    
inputdata = runSimulation(SIMULATION_DAYS)
PlotData(inputdata)

