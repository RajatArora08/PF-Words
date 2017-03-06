from CONSTANTS import PF_TESTED

PF_List = []

with open(PF_TESTED, "r") as file:
    for line in file:
        PF_List.append(line.replace(' ', '_').replace('\n', ''))
