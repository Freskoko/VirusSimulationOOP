import random
import matplotlib.pyplot as plt
import string
from collections import Counter

letters = string.ascii_lowercase

#TODO DO A 10000 DAY SIM! (check time)
#TODO FIX VIRUS PROPERTIES (MAYBE MAKE SUBCLASSES?)

#initial conditions
NUM_PEOPLE = 100000
SICKATDAYZERO = 6
MAXINFECTIONS = 4
SIMULATION_DAYS = 1000
MUTATION_CHANCE = 300000 # 1 in MUTATION CHANCE
PEOPLE_BORN_PERCENT = 2 #fix line 42
LOCKDOWN_REQUIREMENT = 100 #percent
LOCKDOWN_TAKEAWAY = 0 #percent

def RemoveDup(listobj):
    return list(dict.fromkeys(listobj))

def CreateRandomString():
    return( ''.join(random.choice(letters) for i in range(10)) ) 

class Virus:
    def __init__(self,stringid):

        self.stringid = str(stringid)
        self.daysInPerson = 0
        self.incubation_period = random.randint(2,3)

        #wip NOT IMPLEMENTED
        # self.infectivity = random.randint(2,3)
        # self.lethality = random.randint(10,10) #in 
        # self.mutation_chance = MUTATION_CHANCE #implies useful mutation

    def printDays(self):
        return f"days in person = {self.daysInPerson}"

    def returnID(self):
        return str(self.stringid)


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

    Initial_Virus = Virus("FirstVirus")

    for i in range(SICKATDAYZERO):

        PeopleList[i].AddInfection(Initial_Virus)

    returndict = {}
    returndict.setdefault("PeopleList",PeopleList)
            
    return returndict

def RunOneDay(inputdict):
    
    PeopleList = inputdict.get("PeopleList")

    sickcounter = 0
    deathcounter = 0
    lockdown = True

    #find all infections (to check with max later)

    infectionlist = []

    for person in PeopleList:
        if person.dead == False:
            for infection in person.currentInfections:
                g = infection.returnID()
                if g not in infectionlist:
                    infectionlist.append(g)


    #population growth (relative to current pop)
    for i in range(round(  (PEOPLE_BORN_PERCENT/1000)*len(PeopleList)  )): #grows 0.1 per day
        
        Mom = random.choice(PeopleList)
        Dad = random.choice(PeopleList)

        bothimmunities = []
        bothimmunities.extend(Mom.Immunties)
        bothimmunities.extend(Dad.Immunties)

        newperson = PersonInstance()
        newperson.Immunties = bothimmunities
        
        PeopleList.append(newperson)

    #iterate over people and interactions happen

    for person in PeopleList:

        if len(person.currentInfections) > 0 and person.dead == False:

            sickcounter+=1
            
            for viralinfection in person.currentInfections:
            
                #mutation
                if len(infectionlist) <= MAXINFECTIONS:
                    if random.randint(1,MUTATION_CHANCE) == 1:
                        NewVirusName = CreateRandomString()
                        person.AddInfection(Virus(NewVirusName))

                        for i in range(5):

                            Friend = random.choice(PeopleList)
                            if viralinfection.returnID() not in Friend.Immunties and viralinfection not in Friend.Immunties and viralinfection not in Friend.currentInfections:
                                if len(Friend.currentInfections) <= MAXINFECTIONS:
                                    Friend.AddInfection(Virus(NewVirusName)) #tada

                #increment days

                viralinfection.daysInPerson = viralinfection.daysInPerson + 1

                #die or live
                if viralinfection.daysInPerson >= person.immune_response_days:
                            
                    # if person.death_chance <= viralinfection.lethality: #die
                    if person.death_chance == random.randint(1,20):
                        try:
                            # PeopleList.remove(person)
                            deathcounter+=1
                            person.Kill()

                        except Exception as e:
                            pass
                        
                    else: #alive

                        person.addImmunity(viralinfection)
                        person.addImmunity(viralinfection.returnID())
                        person.RemoveInfection(viralinfection)

                #incubation period
                if viralinfection.daysInPerson >= viralinfection.incubation_period:

                    #infect people
                    for _ in range(0,random.randint(0,person.friends)):

                        Friend = random.choice(PeopleList)
                    
                        if viralinfection not in Friend.Immunties and viralinfection not in Friend.currentInfections and Friend.dead == False:
                            if len(Friend.currentInfections) <= MAXINFECTIONS:
                                #chance to infect 
                                if random.randint(1,3) == 1:

                                    name = viralinfection.returnID()

                                    Friend.AddInfection(Virus(name)) #tada


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
    PeopleAliveList = []

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

        AlivePeople = list(a for a in PeopleList if a.dead == False)
        PeopleAliveList.append(len(AlivePeople))

        LargeList_OfInfections = []

        for person in PeopleList:
            for infection in person.currentInfections:
                # if len(person.currentInfections) > 10:
                #     print(len(person.currentInfections))
                if person.dead == False:
                    g = infection.returnID()
                    LargeList_OfInfections.append(g)

        print(f" number of infections currently in people  {len(LargeList_OfInfections)}") #ok so a lot of infections getting addded here 

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
    returndict.setdefault("PeopleAliveList",PeopleAliveList)

    # print(cnt)
    
    return returndict

def PlotData(inputdict):

    print("Plotting Started")

    virusdatadict = inputdict.get("virusdatadict")

    print(virusdatadict)

    plt.plot(inputdict.get("SickPPLperday"), "om")
    plt.plot(inputdict.get("PeopleAliveList"),label="AlivePeople")
    plt.plot(inputdict.get("deadPPLperday"), "r--") #red

    for key,val in virusdatadict.items():
        xs = [x for x, y in val]
        ys = [y for x, y in val]     
        if len(xs) > 50:
            plt.plot(xs,ys,label=f"{key} | {len(xs)}")
        else:
            plt.plot(xs,ys)

    death = inputdict.get("deadPPLperday")

    plt.suptitle(f"Virus simulation")
    plt.title(f"Conditions: {NUM_PEOPLE} people | {SICKATDAYZERO} sick at day 1 | total dead:{sum(death)} | {(sum(death)/NUM_PEOPLE)*100}%",fontsize=10)
    plt.xlabel("Days since first infection")
    plt.ylabel("Amount of people infected")

    plt.legend()

    plt.savefig(f"newimages/virusfigV6.{CreateRandomString()}.png")

    print("Plotting Complete")
    plt.show()
    
inputdata = runSimulation(SIMULATION_DAYS)
PlotData(inputdata)

#466 158 in wip

#52 774 all good

