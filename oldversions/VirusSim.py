import random
import matplotlib.pyplot as plt

#initial conditions
NUM_PEOPLE = 5000
SICKATDAYZERO = 3
INCUBATION_PERIOD = 2
SIMULATION_DAYS = 200




class Person():
    def __init__(self,sick):
        self.sick = sick
        self.days_sick = 0
        self.immune_response_days = random.randint(5,7)
        self.immunity = False
        self.friends=random.randint(1,3)
        # self.friends = 1

    def FindSick(self):
        return self.sick

def StartSimulation():
    PeopleList = []
    for i in range(NUM_PEOPLE):
        PeopleList.append(Person(sick=False))

    for i in range(SICKATDAYZERO):
        PeopleList[i] = Person(sick=True)
            
    return PeopleList

def RunOneDay(PeopleList):

    sickcounter = 0

    for person in PeopleList:
        
        if person.sick == True:
            sickcounter += 1
            #make immune if sick many days
            if person.days_sick >=  person.immune_response_days:
                person.sick = False
                person.immunity = True
                person.days_sick = 0

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
                        coinflip = random.choice([0, 1,2]) #(33%)

                        if coinflip == 1:
                            Friend.sick = True   

    return PeopleList,sickcounter

def runSimulation(days):
    SickPPLperday = []
    data = RunOneDay(StartSimulation())
    for i in range(days):

        data = RunOneDay(data[0])

        SickPPLperday.append(data[1])

    return SickPPLperday

def PlotData(data):
    plt.plot(data)
    plt.suptitle(f"Virus simulation")
    plt.title(f"Conditions: {NUM_PEOPLE} people | {SICKATDAYZERO} sick at day 1 | {INCUBATION_PERIOD} days incubation period",fontsize=10)
    plt.xlabel("Days since first infection")
    plt.ylabel("Amount of people infected")
    plt.savefig("data/virusfig")
    plt.show()
    

PlotData(runSimulation(SIMULATION_DAYS))

#TODO = graph/lockdown/natural immunity/virus mutation
    