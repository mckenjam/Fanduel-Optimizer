import pandas as pd
from mip import Model, xsum, maximize, BINARY

fanduel_df = pd.read_csv("fanduel_players.csv")
fanduel_df = fanduel_df.fillna(0)

# Arrays of costs and points per position
QBcost = fanduel_df['QBcost'].tolist()
QBpoints = fanduel_df['QBpoints'].tolist()
RBcost = fanduel_df['RBcost'].tolist()
RBpoints = fanduel_df['RBpoints'].tolist()
WRcost = fanduel_df['WRcost'].tolist()
WRpoints = fanduel_df['WRpoints'].tolist()
TEcost = fanduel_df['TEcost'].tolist()
TEpoints = fanduel_df['TEpoints'].tolist()
DEFcost = fanduel_df['DEFcost'].tolist()
DEFpoints = fanduel_df['DEFpoints'].tolist()

QBname = fanduel_df['QB'].tolist()
RBname = fanduel_df['RB'].tolist()
WRname = fanduel_df['WR'].tolist()
TEname = fanduel_df['TE'].tolist()
DEFname = fanduel_df['DEF'].tolist()

# Overall draft budget
budget = 60000

# Normalize all the lists to be the same lengths
max_list_length = max(len(QBcost), len(RBcost), len(WRcost), len(TEcost), len(DEFcost))

for i in [QBcost, RBcost, WRcost, TEcost, DEFcost]:
	for j in range(max_list_length-len(i)):
		i.append(0)
for i in [QBpoints, RBpoints, WRpoints, TEpoints, DEFpoints]:
	for j in range(max_list_length-len(i)):
		i.append(0)

max_list_length = range(max_list_length)

# Initialize the model
m = Model("fanduel")

# Declare decision variables
QB = [m.add_var(var_type=BINARY) for i in max_list_length]
RB1 = [m.add_var(var_type=BINARY) for i in max_list_length]
RB2 = [m.add_var(var_type=BINARY) for i in max_list_length]
WR1 = [m.add_var(var_type=BINARY) for i in max_list_length]
WR2 = [m.add_var(var_type=BINARY) for i in max_list_length]
WR3 = [m.add_var(var_type=BINARY) for i in max_list_length]
TE = [m.add_var(var_type=BINARY) for i in max_list_length]
FLEXRB = [m.add_var(var_type=BINARY) for i in max_list_length]
FLEXWR = [m.add_var(var_type=BINARY) for i in max_list_length]
DEF = [m.add_var(var_type=BINARY) for i in max_list_length]

# Objective is to maximize points
m.objective = maximize(xsum(QB[i]*QBpoints[i] + 
							RB1[i]*RBpoints[i] + \
							RB2[i]*RBpoints[i] + \
							WR1[i]*WRpoints[i] + \
							WR2[i]*WRpoints[i] + \
							WR3[i]*WRpoints[i] + \
							TE[i]*TEpoints[i] + \
							FLEXRB[i]*TEpoints[i] + \
							FLEXWR[i]*TEpoints[i] + \
							DEF[i]*TEpoints[i] for i in max_list_length))


# Only pick one of each position
m += xsum(QB[i] for i in max_list_length) == 1
m += xsum(RB1[i] for i in max_list_length) == 1
m += xsum(RB2[i] for i in max_list_length) == 1
m += xsum(WR1[i] for i in max_list_length) == 1
m += xsum(WR2[i] for i in max_list_length) == 1
m += xsum(WR3[i] for i in max_list_length) == 1
m += xsum(TE[i] for i in max_list_length) == 1
m += xsum(DEF[i] for i in max_list_length) == 1

m += xsum(FLEXRB[i] + FLEXWR[i] for i in max_list_length) == 1

# Cannot pick the same player twice
for i in max_list_length:
	m += RB1[i] + RB2[i] + FLEXRB[i] <= 1
	m += WR1[i] + WR2[i] + WR3[i] + FLEXWR[i] <= 1

# Budget constraints
m += xsum(QB[i]*QBcost[i] + \
		  RB1[i]*RBcost[i] + \
		  RB2[i]*RBcost[i] + \
		  WR1[i]*WRcost[i] + \
		  WR2[i]*WRcost[i] + \
		  WR3[i]*WRcost[i] + \
		  TE[i]*TEcost[i] + \
		  FLEXRB[i]*RBcost[i] + \
		  FLEXWR[i]*WRcost[i] + \
		  DEF[i]*DEFcost[i] for i in max_list_length) <= budget

# Must pick a player for every position
m += xsum(QB[i]*QBcost[i] for i in max_list_length) >= 1
m += xsum(RB1[i]*RBcost[i] for i in max_list_length) >= 1
m += xsum(RB2[i]*RBcost[i] for i in max_list_length) >= 1
m += xsum(WR1[i]*WRcost[i] for i in max_list_length) >= 1
m += xsum(WR2[i]*WRcost[i] for i in max_list_length) >= 1
m += xsum(WR3[i]*WRcost[i] for i in max_list_length) >= 1
m += xsum(TE[i]*TEcost[i] for i in max_list_length) >= 1
m += xsum(FLEXRB[i]*RBcost[i] + FLEXWR[i]*WRcost[i] for i in max_list_length) >= 1
m += xsum(DEF[i]*DEFcost[i] for i in max_list_length) >= 1

m.optimize()

total_points = 0
total_costs = 0

for itr, i in enumerate(max_list_length):
	if QB[i].x == 1:
		print("QB: " + str(QBname[itr]))
		total_points += QBpoints[itr]
		total_costs += QBcost[itr]
for itr, i in enumerate(max_list_length):
	if RB1[i].x == 1:
		print("RB1: " + str(RBname[itr]))
		total_points += RBpoints[itr]
		total_costs += RBcost[itr]
for itr, i in enumerate(max_list_length):
	if RB2[i].x == 1:
		print("RB2: " + str(RBname[itr]))
		total_points += RBpoints[itr]
		total_costs += RBcost[itr]
for itr, i in enumerate(max_list_length):
	if WR1[i].x == 1:
		print("WR1: " + str(WRname[itr]))
		total_points += WRpoints[itr]
		total_costs += WRcost[itr]
for itr, i in enumerate(max_list_length):
	if WR2[i].x == 1:
		print("WR2: " + str(WRname[itr]))
		total_points += WRpoints[itr]
		total_costs += WRcost[itr]
for itr, i in enumerate(max_list_length):
	if WR3[i].x == 1:
		print("WR3: " + str(WRname[itr]))
		total_points += WRpoints[itr]
		total_costs += WRcost[itr]
for itr, i in enumerate(max_list_length):
	if TE[i].x == 1:
		print("TE: " + str(TEname[itr]))
		total_points += TEpoints[itr]
		total_costs += TEcost[itr]
for itr, i in enumerate(max_list_length):
	if FLEXRB[i].x == 1:
		print("FLEX: " + str(RBname[itr]))
		total_points += RBpoints[itr]
		total_costs += RBcost[itr]
for itr, i in enumerate(max_list_length):
	if FLEXWR[i].x == 1:
		print("FLEX: " + str(WRname[itr]))
		total_points += WRpoints[itr]
		total_costs += WRcost[itr]
for itr, i in enumerate(max_list_length):
	if DEF[i].x == 1:
		print("DEF: " + str(DEFname[itr]))
		total_points += DEFpoints[itr]
		total_costs += DEFcost[itr]

print("Total Points: "+str(total_points))
print("Total Cost: "+str(total_costs))