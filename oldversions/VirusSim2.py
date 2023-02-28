import random
import matplotlib.pyplot as plt

#initial conditions
NUM_PEOPLE = 50000
SICKATDAYZERO = 3
INCUBATION_PERIOD = 3
SIMULATION_DAYS = 700
MUTATION_CHANCE = 1 # in 100
PEOPLE_BORN_PERCENT = 1 #fix line 42
LOCKDOWN_REQUIREMENT = 35 #percent
LOCKDOWN_TAKEAWAY = 2 #percent

class Virus():
    def __init__(self):
        self.mutation_chance = MUTATION_CHANCE #implies useful mutation 

class Person():
    def __init__(self,sick):
        self.sick = sick
        self.days_sick = 0
        self.immune_response_days = random.randint(5,12)
        self.immunity = False
        self.friends=random.randint(2,15)
        self.death_chance = random.randint(1,90) #person.death_chance <= random.randint(1,100)

    def FindSick(self):
        return self.sick

def StartSimulation():
    PeopleList = []
    VirusList = []

    for i in range(NUM_PEOPLE):
        PeopleList.append(Person(sick=False))

    for i in range(SICKATDAYZERO):
        PeopleList[i] = Person(sick=True)
        VirusList.append(Virus())

    returndict = {}
    returndict.setdefault("PeopleList",PeopleList)
    returndict.setdefault("VirusList",VirusList)
            
    return returndict

def RunOneDay(inputdict):

    PeopleList = inputdict.get("PeopleList")
    VirusList = inputdict.get("VirusList")

    for _ in range(1, round(len(PeopleList)/10000)): #population growth
        PeopleList.append(Person(sick=False))

    for virus in VirusList:

        if virus.mutation_chance == random.randint(1,100):
            print("MUTATED",end=" ")
            
            for person in PeopleList:

                if random.randint(1,10) > 9: #mutation causes immunity to go away for most people (90%)

                    person.immunity = False

                    if person.sick == True: #if they sick then it will take longer to be immune to this sickness
                        person.immune_response_days += random.randint(5,12) #so they will have to 
                    

    sickcounter = 0
    deathcounter = 0
    lockdown = True

    for person in PeopleList:
        
        if person.sick == True:
            sickcounter += 1
            #make immune/die if sick many days
            if person.days_sick >=  person.immune_response_days:

                if person.death_chance <= random.randint(1,100): #die
                    PeopleList.remove(person)
                    deathcounter+=1

                else: #alive
                    person.sick = False
                    person.immunity = True
                    person.immune_response_days += person.days_sick

        if person.sick == True:
            #increment sick counter
            person.days_sick += 1

            #incubation period
            if person.days_sick >= INCUBATION_PERIOD:

                #infect people
                for _ in range(0,random.randint(0,person.friends)):

                    Friend = random.choice(PeopleList)

                    if Friend.immunity == False:
                        
                        #chance to infect 
                        coinflip = random.choice([0, 1, 2]) #(n/100)%

                        if coinflip == 1:
                            Friend.sick = True   

    if LOCKDOWN_REQUIREMENT >= (sickcounter/NUM_PEOPLE)*100:
        for person in PeopleList:
            person.friends=random.randint(1,2)
        lockdown = True

    elif LOCKDOWN_TAKEAWAY >= (sickcounter/NUM_PEOPLE)*100:
        for person in PeopleList:
            person.friends=random.randint(4,10)
        lockdown = False

    returndict = {}
    returndict.setdefault("PeopleList",PeopleList)
    returndict.setdefault("VirusList",VirusList)
    returndict.setdefault("sickcounter",sickcounter)
    returndict.setdefault("deathcounter",deathcounter)
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

    datadict = RunOneDay(StartSimulation())

    for i in range(days):

        datadict = RunOneDay(datadict)
        day = datadict.get("currentday")

        print(f" DAY {day} of {days} COMPLETED")

        SickPPLperday.append(datadict.get("sickcounter"))
        deadPPLperday.append(datadict.get("deathcounter"))
        lockdownlist.append(datadict.get("lockdown"))


    returndict = {}
    returndict.setdefault("SickPPLperday",SickPPLperday)
    returndict.setdefault("deadPPLperday",deadPPLperday)
    returndict.setdefault("lockdownlist",lockdownlist)
    
    return returndict

def PlotData(inputdict):

    print("Plotting Started")

    plt.plot(inputdict.get("SickPPLperday"))
    plt.plot(inputdict.get("deadPPLperday"))
    plt.plot(inputdict.get("lockdownlist"))

    death = inputdict.get("deadPPLperday")

    plt.suptitle(f"Virus simulation")
    plt.title(f"Conditions: {NUM_PEOPLE} people | {SICKATDAYZERO} sick at day 1 | {INCUBATION_PERIOD} days incubation period | total dead:{sum(death)} | {(sum(death)/NUM_PEOPLE)*100}%",fontsize=10)
    plt.xlabel("Days since first infection")
    plt.ylabel("Amount of people infected")
    plt.savefig("data/virusfig2")

    print("Plotting Complete")
    plt.show()
    

inputdata = runSimulation(SIMULATION_DAYS)
PlotData(inputdata)


#TODO FIX TO RUN MULTIPLE SIMS

#SIMULATE MULTIPLE VIRUS OCCOURENCES? MAKE NEW VIRUS (WITH NEW ID? WITH DIFFERENT PROPERTIES )