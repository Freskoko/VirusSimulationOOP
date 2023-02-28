import random
import matplotlib.pyplot as plt
import string
from collections import Counter

letters = string.ascii_lowercase

#TODO ADD MUTSTION + ADD ABLE TO TRACK VIRUS THAT COEM LATER (FROM DAY 20 FOR ECXAMPLE (USE TUPLES))


#initial conditions
NUM_PEOPLE = 50000
SICKATDAYZERO = 10
SIMULATION_DAYS = 85
MUTATION_CHANCE = 1 # in 100
# PEOPLE_BORN_PERCENT = 1 #fix line 42
LOCKDOWN_REQUIREMENT = 100 #percent
LOCKDOWN_TAKEAWAY = 0 #percent

def CreateRandomString():
    return( ''.join(random.choice(letters) for i in range(10)) ) 

class Virus():
    def __init__(self,stringid):

        self.mutation_chance = MUTATION_CHANCE #implies useful mutation
        self.stringid = stringid
        self.lethality = random.randint(10,10) #in 
        self.daysInPerson = 0
        self.incubation_period = random.randint(2,2)

        #wip NOT IMPLEMENTED
        # self.infectivity = random.randint(2,3)

    def printDays(self):
        return f"days in person = {self.daysInPerson}"

    def returnID(self):
        return f"{self.stringid}"
        

class PersonInstance():
    def __init__(self):

        self.currentInfections = []
        self.Immunties = []
        #---
        self.immune_response_days = random.randint(5,7) 
        self.friends=random.randint(2,8)
        # self.death_chance = random.randint(1,25) 
        self.death_chance = 1

        self.dead = False

    def AddInfection(self,infection):
        self.currentInfections.append(infection)   
    
    def RemoveInfection(self,infection):
        self.currentInfections.remove(infection)

    def addImmunity(self,infection):
        self.Immunties.append(infection)

    def Kill(self):
        self.dead = True

    def printInfections(self):
        return self.currentInfections


def StartSimulation():
    PeopleList = []
    
    for i in range(NUM_PEOPLE):
        PeopleList.append(PersonInstance())

    Initial_Virus = Virus("FirstVirus")

    for i in range(SICKATDAYZERO):

        PeopleList[i].AddInfection(Initial_Virus)

    
    Initial_Virus2 = Virus("SecondVirus")

    for i in range(SICKATDAYZERO):

        PeopleList[-i].AddInfection(Initial_Virus2)

    Initial_Virus3 = Virus("ThirdVirus")

    for i in range(SICKATDAYZERO):

        PeopleList[i+50].AddInfection(Initial_Virus3)

    returndict = {}
    returndict.setdefault("PeopleList",PeopleList)
            
    return returndict

def RunOneDay(inputdict):
    
    PeopleList = inputdict.get("PeopleList")

    sickcounter = 0
    deathcounter = 0
    lockdown = True

    #iterate over people and interactions happen

    #TODO ADD MUTATION! 

    for person in PeopleList:
    
        if len(person.currentInfections) > 0 and person.dead == False:

            sickcounter+=1
            
            for viralinfection in person.currentInfections:

                viralinfection.daysInPerson = viralinfection.daysInPerson + 1

                # print(viralinfection.printDays())

                #make immune/die if sick many days
                if viralinfection.daysInPerson >= person.immune_response_days:

                    # if person.death_chance <= viralinfection.lethality: #die
                    if person.death_chance == random.randint(1,3):
                        try:
                            PeopleList.remove(person)
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

                        try:
                            Friend = random.choice(PeopleList)

                            if viralinfection not in Friend.Immunties and viralinfection not in Friend.currentInfections:
                                
                                #chance to infect 
                                if random.randint(1,6) == 1:

                                    Friend.AddInfection(Virus(viralinfection.returnID())) #tada
                        except Exception as e:
                            pass

    #--------------

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

        print(f" DAY {day} of {days} COMPLETED")

        SickPPLperday.append(datadict.get("sickcounter"))
        deadPPLperday.append(datadict.get("deathcounter"))
        lockdownlist.append(datadict.get("lockdown"))

        #get data from person list and count which infections!

        PeopleList = datadict.get("PeopleList")

        LargeList_OfInfections = []

        for person in PeopleList:
            for infection in person.currentInfections:
                g = infection.returnID()
                LargeList_OfInfections.append(g)

        cnt = Counter()
        
        for word in LargeList_OfInfections:
            cnt[word] += 1

        for virusName,virusCount in cnt.items():
            if virusName in virusdatadict:
                virusdatadict[virusName].append(virusCount)

            if virusName not in virusdatadict:
                virusdatadict.setdefault(virusName,[virusCount])

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

    print(virusdatadict)

    for key,val in virusdatadict.items():
        plt.plot(val)

    plt.plot(inputdict.get("deadPPLperday"), "r--") #red
    # plt.plot(inputdict.get("lockdownlist"))

    death = inputdict.get("deadPPLperday")

    plt.suptitle(f"Virus simulation")
    plt.title(f"Conditions: {NUM_PEOPLE} people | {SICKATDAYZERO} sick at day 1 | total dead:{sum(death)} | {(sum(death)/NUM_PEOPLE)*100}%",fontsize=10)
    plt.xlabel("Days since first infection")
    plt.ylabel("Amount of people infected")
    plt.savefig("data/virusfig3")

    print("Plotting Complete")
    plt.show()
    
inputdata = runSimulation(SIMULATION_DAYS)
PlotData(inputdata)


#TODO FIX TO RUN MULTIPLE SIMS

#SIMULATE MULTIPLE VIRUS OCCOURENCES? MAKE NEW VIRUS (WITH NEW ID? WITH DIFFERENT PROPERTIES )