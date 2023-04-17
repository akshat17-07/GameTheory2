import random
import csv

def create_groups(nums, l1):
    """
    This function help to create groups
    """
    groups = []
    x=0
    for i in range(nums):
        groups.append([])
        for j in range(l1[i]):
            groups[i].append(x)
            x+=1        
    return groups

def one_day(groups, number_resturants):
    winner = list()
    rest = {}
    selection = list()
    # creating returant matrix
    for i in range(number_resturants):
        rest[i] = []
        selection.append(i)
    
    for i in groups:
        new_set = selection.copy()
        for j in i:
            r = random.choice(new_set)
            new_set.remove(r)
            rest[r].append(j)
    
    for i in rest:
        if rest[i] != list():
            winner.append(random.choice(rest[i]))
    return winner

def hund_days(groups, number_resturants):
    """
    This function runs simulation for 100 days
    """
    # creating probality dic
    probality = {}
    x = 0
    for i in groups:
        for j in i:
            probality[x] = 0
            x+=1
            
    for i in range(100):
        
        temp = one_day(groups, number_resturants)
        
        for j in groups:
            
            if len(j) != 0:
                winners = 0
                losers = 0
                
                for k in j:
                    if k in temp:
                        winners += 1
                    else:
                        losers += 1
                
                tax_cut = losers/(losers+winners)
                    
                check = 0
                for k in j:
                        probality[k]  += 1 - tax_cut
                        check += 1 - tax_cut
    return probality
    
def find_index(player, groups):
    """This is a helper function of reorder. it find and return the index in groups of player"""
    for i in range(len(groups)):
        if player in groups[i]:
            return i
            
def reorder(groups, probablity, agents,change):
    """this function reorders the groups based on probablity"""
    bracket = list(range(0,agents))
    random.shuffle(bracket)
    
    while len(bracket) > 2:
        temp1 = random.randint(0,len(bracket)-1)
        temp2 = random.randint(0,len(bracket)-1)
        if temp1 != temp2:
            if temp1 > temp2:
                index = temp2
            else:
                index = temp1
            
            if probablity[bracket[temp1]] - probablity[bracket[temp2]] > change :
                winner = bracket[temp1]
                lose = bracket[temp2]
            elif probablity[bracket[temp2]] - probablity[bracket[temp1]] > change :
                winner = bracket[temp2]
                lose = bracket[temp1]
            else:
                winner = None
                
            if winner != None:
                group1 = find_index(winner, groups)
                group2 = find_index(lose, groups)
                groups[group2].remove(lose)
                groups[group1].append(lose)
            player1 = bracket[temp1]
            player2 = bracket[temp2]
            
            if index != 0:
                bracket.remove(bracket[index-1])
            bracket.remove(player1)
            bracket.remove(player2)
    
    return groups

def run(groups, tol, number_resturants, agents):
    """
    This function controls the simulation
    """
    temp = groups
    success = 0
    for i in range(1000):
        if temp == groups:
            success += 1
        else:
            success = 1
        temp = groups
        if success > 20: 
            break
        # running simulation for 100 days
        probablity = hund_days(groups, number_resturants)
        groups = reorder(groups, probablity, agents,tol)
    return groups

if __name__ == "__main__":
    groups = create_groups(2,[50,50])
    agents = 0
    for i in groups:
        for j in i:
            agents += 1
    
    rows = [["tol", "group_1_size"]]
    iterates = []
    
    for i in range(1001):
        iterates.append(i*0.1)
    
    for i in iterates:
        copy = create_groups(2,[50,50])
        temp = run(copy, i, 100, agents)
        rows.append([i, len(temp[0])])
    
    
    with open("result", 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        # writing the data rows
        for i in rows:
            csvwriter.writerow(i)
    