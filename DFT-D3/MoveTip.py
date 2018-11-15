filename = "AboveCe.xyz"


Tipz = 5

Atom = []
x = []
y = []
z = []
NumberofAtoms = 0

with open(filename, 'r') as f:
    next(f)  # skip 1 line
    next(f)  # skip another one.
    for line in f:
        Atom.append(line.split()[0])
        x.append(float(line.split()[1]))
        y.append(float(line.split()[2]))
        z.append(float(line.split()[3]))

HighestO = 0
Oi = 0

counter = 0
for i in Atom:
    if i == "H":
        z[counter] += Tipz

    if i == "Si":
        z[counter] += Tipz

    if i == "O":
        if HighestO > z[counter]:
            HighestO = z[counter]
            Oi = counter
    counter += 1

counter -= 1


z[counter] += Tipz


f = open(filename.split('.')[0] + str(Tipz*10) +
         "." + filename.split('.')[1], 'w')

f.write(str(len(Atom))+"\n")
f.write("\n")


counter = 0
for i in Atom:
    f.write(str(i) + " " + str(x[counter]) + " " +
            str(y[counter]) + " " + str(z[counter]) + " \n")
    counter += 1
