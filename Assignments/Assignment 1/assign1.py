
###################################################################
#
#   CSSE1001/7030 - Assignment 1
#
#   Student Number: s4356917
#
#   Student Name: Elliot Randall
#
###################################################################

#####################################
# Support given below - DO NOT CHANGE
#####################################

from assign1_support import *

#####################################
# End of support 
#####################################


def load_data(dateStr):
    """
    Takes a string representing a date in the correct format and returns a list
    of data for each minute of the day in time order. 

    Precondition: The user enters a string that is in the valid date format
    of dd-mm-yy.

    load_data(str) -> list<tuple<string, float, float,tuple<multiple ints>>>
    """
    data = get_data_for_date(dateStr)
    elem = data.split("\n")
    dlist = []
    for i in elem:
        split = i.split(',')
        if len(i) == 0:
            break #If there is nothing in the tuple, remove it. 
        time = split[0]
        temp = float(split[1])
        sunlight = float(split[2])
        length = len(split)
        measure = []#Power measurements for each array. 
        for n,s in enumerate(split):#Adds the power measurement to a tuple.
            if n > 2:
                measure.append(int(split[n]))
        measure = tuple(measure)
        dlist.append((time, temp, sunlight, measure))
    return dlist


def max_temp(data):
    """
    Retrieves the maximum daily temperature from load_data function and
    returns a pair consisting of the maximum temperature and a list of times
    at which the temperature was maximum.

    From the data generated and formatted in the load_data function,
    this function finds the maximum temperature recorded. 

    max_temp(list) -> tuple<float, list<str>>
    """
    temp = -273#Absolute 0. 
    times = []
    for t in data:
        if t[1] > temp:
            temp = t[1]
    for t in data:
        if t[1] == temp:
            times.append(t[0])
    maxrec = (temp, times)
    return maxrec


def total_energy(data):
    """
    Calculates the total energy produced from load_data function in
    one day from all of the PV units in kWh.

    total_energy(list) -> float
    """
    energy = 0
    for i in data:
        energy = energy + sum(i[3])
    return float(energy)/60000


def max_power(data):
    """
    Takes data produced from load_data() function and returns the power produced
    by each PV unit in kilowatts. 
    
    max_power(list) -> list<tuple<str, float>>
    """
    maxes = [0] * len(ARRAYS) 
    parray = []
    for row in data:
        powers = row[3]
        for i, power in enumerate(powers):
            if power > maxes[i]:
                maxes[i] = power
        fmaxes = [x/float(1000) for x in maxes]#Divide values by 1000 in maxes
    parray = list(zip(ARRAYS, fmaxes))#Create a list with tuples including ARRAYS and fmaxes     
    return parray


def display_stats(dateStr):
    """
    Displays max temp, total enery and max power derived from load_data() function.

    display_stats(str) -> None
    """
    data = load_data(dateStr)
    print ""
    print "Statistics for",dateStr, "\n"
    print "Maximum Temperature:", str(max_temp(data)[0]) + "C at times", ', '.join(max_temp(data)[1]), "\n"
    print "Total Energy Production:",str(("{0:.1f}".format(round(total_energy(data),1))))+"kWh", "\n"
    print "Maximum Power Outputs:","\n"
    for i, n in max_power(data):
        print STATS_ROW.format(i, n)
    print ""


    
def interact():
    """
    An interactive function that allows the user to view data by command in a text
    based interface.

    The user enters "date" and then a valid dateStr in the format of dd-mm-yy. 

    interact() -> None
    """
    print "Welcome to PV calculator"
    print "\n"
    while True:
        inputt = raw_input("Command: ")
        isplit = inputt.split(" ")
        if inputt == "q":
            break
        try: 
            kdate = isplit[0]
            dateStr = isplit[1]
        except IndexError:#Error if not enough input. 
            print "Unknown Command: "+inputt+'\n'
            continue
        try: 
            if len(isplit) > 2:
                print "Unknown Command: " + inputt+'\n'
            elif 'date' == kdate:
                str(display_stats(dateStr))+"\n"
            else:
                print "Unknown Command: "+ inputt+'\n'
        except ValueError:#Error if date is entered incorrectly. 
            print "Unknown Command:", inputt+'\n'
            
            
            


    



##################################################
# !!!!!! Do not change (or add to) the code below !!!!!
# 
# This code will run the interact function if
# you use Run -> Run Module  (F5)
# Because of this we have supplied a "stub" definition
# for interact above so that you won't get an undefined
# error when you are writing and testing your other functions.
# When you are ready please change the definition of interact above.
###################################################

if __name__ == '__main__':
    interact()

