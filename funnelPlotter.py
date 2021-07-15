import sys
import matplotlib as mlt
import matplotlib.pyplot as plt
'''
This is a small program that inputs the score.sc (even the littel weird ones), 
name_of_the_image_file, and the limit_of_energy file via command line and plots 
the energy-rmsd.
'''

if len(sys.argv) != 4: 
    raise ValueError('Please provide the valid command line arguments')
file = sys.argv[1]
name = sys.argv[2]
limit = sys.argv[3]
limit = float(limit)

res = []
x_total = []
x_sugar = []
y = []

with open(file,'r') as f:
    count = -1
    for line in f:
        count += 1
        if count >= 2:
            line = line.split()
            if len(line) == 0: break
            energy = line[1]
            sugar_rmsd = line[22]
            total_rmsd = line[23]
            length = len(line[-1])
            residue = line[-1][length-4:length]
            if int(residue) in res:
                x_pos = res.index(int(residue))
                x_total[x_pos] = float(total_rmsd)
                x_sugar[x_pos] = float(sugar_rmsd)
                y[x_pos] = float(energy)
            else:
                res.append(int(residue))
                x_total.append(float(total_rmsd))
                x_sugar.append(float(sugar_rmsd)) 
                y.append(float(energy))

print("length of the x axis is: ", len(x_sugar), " and the length of the y axis is: ", len(y))

x_total_final = []
x_sugar_final = []
y_final = [] # here y stands for energy 

for i in range(0,len(x_sugar)):
    if y[i] < limit:
        x_total_final.append(x_total[i])
        x_sugar_final.append(x_sugar[i])
        y_final.append(y[i])

fig = plt.figure(figsize=(7,5))
plt.scatter(x_sugar_final,y_final)
plt.xlabel('sugar-RMSD')
plt.ylabel('Rosetta Energy Unit (REU)')
plt.title(name + "-sugar")
fig.savefig(name + "-sugar")

fig2 = plt.figure(figsize=(7,5))
plt.scatter(x_total_final, y_final)
plt.xlabel('total-RMSD')
plt.ylabel('Rosetta Energy Unit (REU)')
plt.title(name + "-total")
fig2.savefig(name + "-total")

## Print the top 10 residues in terms of teh energy units 
energy_tuples = []
def takeEnergy(elem):
    return elem[1]

for i in range(len(y)): energy_tuples.append((res[i], y[i]))
energy_tuples.sort(key=takeEnergy)

print("")
print("Top 10 residues are: ")
print("residue, energy")
for i in range(10):
    print(energy_tuples[i])

print("")
print("The residue with the minimum energy is: ", res[y.index(min(y))])
print("")
