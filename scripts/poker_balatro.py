"""Lit module to generate all poker combos
Created : 05/09/2024
"""
import itertools
import pandas as pd
def high_card_combo(values):
    list = []
    for v in values:
        list.append([v])
    return list

def pair_combo(values):
    list =[]
    for v in values:
        list.append([v,v])
    return list

def three_of_a_kind_combo(values):
    list =[]
    for v in values:
        list.append([v,v,v])
    return list

   
def two_pair_combo(values):
    combos =  list(itertools.combinations(values, 2))
    return combos

def four_of_a_kind_combo(values):
    list =[]
    for v in values:
        list.append([v,v,v,v])
    return list

def straight_combo(values):
    choices = len(values)-4
    combos = []
    for x in range(choices):
        list = []
        for y in range(5):
            list.append(values[x+y])
        combos.append(list)
    combos.append(['A','2','3','4','5'])
    return combos

# Becarefull it returns the straight flush too
def flush_combo(values):
    combos = list(itertools.combinations(values, 5))
    for combo in combos:
        if combo == ('2', '3', '4', '5', 'A'):
            combos.remove(combo)
        for c in straight_combo(values):
            if c == list(combo):
                combos.remove(combo)

            
    return combos


def full_house_combo(values):
    combos =  list(itertools.combinations(values, 2))
    magic = []
    for combo in combos:
        magic.append([combo[0],combo[0],combo[0],combo[1],combo[1]])
        magic.append([combo[1],combo[1],combo[1],combo[0],combo[0]])
    return magic
    
def straight_flush_combo(values):
    return straight_combo(values)
    
    
def get_combo(hand_name, values):
    match hand_name:
        case "High card":
            return high_card_combo(values)
        case "One pair":
            return pair_combo(values)
        case "Three of a kind":
            return three_of_a_kind_combo(values)
        case "Four of a kind":
            return four_of_a_kind_combo(values)
        case "Two pair":
            return two_pair_combo(values)
        case "Flush":
            return flush_combo(values)
        case "Straight":
            return straight_combo(values)
        case "Straight flush":
            return straight_flush_combo(values)
        case "Full house":
            return full_house_combo(values)
        case _:
            print("Warning warning warning bzzzzttt")
            
def high_card(values):
    stats = [0,0,0]
    total = sum(values)
    average = total/len(values)
    stats[0] = values[0]
    stats[1] = values[len(values) -1 ]
    stats[2] = round(average,2)
    return stats
    
def pair(values):
    stats = [0,0,0]
    total = sum(values)*2
    average = total/len(values)
    stats[0] = values[0] * 2
    stats[1] = values[len(values) -1 ] *2
    stats[2] = round(average,2)
    return stats
    
def three_of_a_kind(values):
    stats = [0,0,0]
    total = sum(values)*3
    average = total/len(values)
    stats[0] = values[0] * 3
    stats[1] = values[len(values) -1 ] *3
    stats[2] = round(average,2)
    return stats

def four_of_a_kind(values):
    stats = [0,0,0]
    total = sum(values)*4
    average = total/len(values)
    stats[0] = values[0] * 4
    stats[1] = values[len(values) -1 ] *4
    stats[2] = round(average,2)
    return stats
    
def two_pair(values):
    stats = [0,0,0]
    all_combos =  list(itertools.combinations(values, 2))
    sum = 0
    stats[0] = values[0] *2  + values[1] * 2
    stats[1] = values[len(values) -1]  *2  + values[len(values) -2]  * 2
    
    for combo in all_combos:
        sum += (combo[0]*2) + (combo[1]*2)
    average = sum /len(all_combos)
    stats[2] = round(average,2)
    return stats
 
def straight(values):
    stats = [0,0,0]
    choices = len(values)-4
    _sum = 0
    for x in range(choices):
        list = []
        for y in range(5):
            list.append(values[x+y])
        _sum += sum(list)
    average = _sum/choices
    
    stats[0] = values[0] + values[1] +values[2] +values[3] +values[4]   
    stats[1] = values[len(values) -1] + values[len(values) -2] +values[len(values) -3] +values[len(values) -4] +values[len(values) -5]   
    stats[2] = round(average,2)
    
    return stats




def full_house(values):
    stats = [0,0,0]
    all_combos =  list(itertools.combinations(values, 2))
    _sum = 0
    min = 1000
    max = -1
    for combo in all_combos:
        if (combo[0]*3) + (combo[1]*2) < min:
            min = (combo[0]*3) + (combo[1]*2)
        if (combo[0]*3) + (combo[1]*2) > max:
            max = (combo[0]*3) + (combo[1]*2)
    
    
        _sum += (combo[0]*3) + (combo[1]*2)
        _sum += (combo[0]*2) + (combo[1]*3)
    average = _sum/(len(all_combos)*2)
    
    
    stats[0] = min
    stats[1] = max
    stats[2] = round(average,2)
    
    return stats
    
def flush(values):
    stats = [0,0,0]
    all_combos = list(itertools.combinations(values, 5))
    _sum = 0
    min = 1000
    max = -1
    for combo in all_combos:
        if sum(combo) < min:
            min = sum(combo)
        if sum(combo) > max:
            max = sum(combo)
        _sum += sum(combo)
    average = _sum /len(all_combos)
    
    stats[0] = min
    stats[1] = max
    stats[2] = round(average,2)
    
    
    return stats
   
        

def generate_value_stats(values):
    dataframe = pd.DataFrame( columns=['Poker Hand','min', 'max', 'average'])
    rows = []
    rows.append(['High card'] + high_card(values))
    rows.append(['One pair'] + pair(values))
    rows.append(['Two pair'] + two_pair(values))
    rows.append(['Three of a kind'] + three_of_a_kind(values))
    rows.append(['Straight'] + straight(values))
    rows.append(['Flush'] + flush(values))
    rows.append(['Full house'] + full_house(values))
    rows.append(['Four of a kind'] + four_of_a_kind(values))
    rows.append(['Straight flush'] + straight(values))
    for x in range(len(rows)):
        dataframe.loc[len(dataframe.index)] = rows[x]
    return dataframe






if __name__ == "__main__":
    print("ok")