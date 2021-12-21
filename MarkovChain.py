import numpy as np
import random as rm


states = ["Sleep","Icecream","Run"]

transitionName = [["SS","SR","SI"],["RS","RR","RI"],["IS","IR","II"]]

transitionMatrix = [[0.2,0.6,0.2],[0.1,0.6,0.3],[0.2,0.7,0.1]]

if sum(transitionMatrix[0]) + sum(transitionMatrix[1]) + sum(transitionMatrix[2])!=3 :
   print("Somewhere, something went wrong. Transition matrix, perhaps?")
else: print("All is gonna be okay, you should move on!! ;)")

def activity_forcast(days,activityToday):
    
    # activityToday = "Sleep"
    # print("start state : " + activityToday)

    activityList = [activityToday]

    i = 0 

    prob = 1

    while i != days :
        if activityToday == 'Sleep':
            change = np.random.choice(transitionName[0],replace=True,p=transitionMatrix[0])
            if change == 'SS':
                prob = prob * 0.2
                activityList.append("Sleep")
            elif change == "SR" :
                prob = prob * 0.6
                activityToday = "Run"
                activityList.append("Run")
            else :
                prob = prob * 0.2
                activityToday = "Icecream"
                activityList.append("Icecream")
        elif activityToday == 'Run':
            change = np.random.choice(transitionName[1],replace=True,p=transitionMatrix[1])
            if change == 'RR':
                prob = prob * 0.5
                activityList.append("Run")
            elif change == "RS" :
                prob = prob * 0.2
                activityToday = "Sleep"
                activityList.append("Sleep")
            else :
                prob = prob * 0.3
                activityToday = "Icecream"
                activityList.append("Icecream")
        elif activityToday == 'Icecream':
            change = np.random.choice(transitionName[2],replace=True,p=transitionMatrix[2])
            if change == 'II':
                prob = prob * 0.1
                activityList.append("Icecream")
            elif change == "IS" :
                prob = prob * 0.2
                activityToday = "Sleep"
                activityList.append("Sleep")
            else :
                prob = prob * 0.7
                activityToday = "Run"
                activityList.append("Run")
        
        i += 1
    
    # print("Possible states :"+str(activityList))
    # print("End stats after "+str(days)+" days :"+ activityToday)
    # print("Probability of the possible sequence of states: "+str(prob))

    return activityList

list_activity = []
count_run = 0 
count_icecream = 0
count_sleep = 0

startState = np.random.choice(states,replace=True,p=transitionMatrix[0])

for iteration in range(1,100000) :
    list_activity.append(activity_forcast(2,startState))

for smaller_list in list_activity :
    if smaller_list[2] == "Run":
        count_run += 1
    elif smaller_list[2] == "Icecream":
        count_icecream += 1
    else:
        count_sleep +=1

percentage_run = (count_run/100000) * 100
percentage_sleep = (count_sleep/100000) * 100
percentage_icecream = (count_icecream/100000) * 100
print("The probabily of starting at state : '" + startState + 
"' and ending at 'Run' = " + str(percentage_run) + "% ; ending at 'Iceream' = " + str(percentage_icecream) + "% ; ending at 'Sleep' = " + str(percentage_sleep) + "%")


# activity_forcast(6)