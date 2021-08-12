# all the fasta files are of same length 
# the header can be identified by the ">" in the front of the line 

# a multidimensional array (length of sequence x 20) for storing everything 
class nucleotide:
    def __init__(self, i):
        self.aa = dict()
        self.total = 0
        self.position = i
    def add(self, aa):
        if aa in self.aa.keys():
            self.aa[aa] += 1
        else: 
            self.aa[aa] = 1
        self.total += 1
    def show(self):
        for key in self.aa.keys():
            self.aa[key] /= self.total
            self.aa[key] = round(self.aa[key], 2)
        # print("Pos: ", self.position, ", aa: ", self.aa)

sequence = []

filename = "first_round_seq.fasta"

# reading the .fasta file and parsing through each line 
f = open(filename)
lines = f.readlines()

for line in lines:
    if line[0] != '>': 
        if len(sequence) == 0:
            for i in range(0, len(line)):
                n = nucleotide(i)
                n.add(line[i])
                sequence.append(n)
        else: 
            for i in range(0, len(line)):
                sequence[i].add(line[i])
            
original_seq = "SALNKAPGYQDFPAYYSDSAHADDQVTHPDVVVLEEPWNGYRYWAVYTPNVMRISIYENPSIVASSDGVHWVEPEGLSNPIEPQPPSTRYHNCDADMVYNAEYDAMMAYWNWADDQGGGVGAEVRLRISYDGVHWGVPVTYDEMTRVWSKPTSDAERQVADGEDDFITAIASPDRYDMLSPTIVYDDFRDVFILWANNTGDVGYQNGQANFVEMRYSDDGITWGEPVRVNGFLGLDENGQQLAPWHQDVQYVPDLKEFVCISQCFAGRNPDGSVLHLTTSKDGVNWEQVGTKPLLSPGPDGSWDDFQIYRSSFYYEPGSSAGDGTMRVWYSALQKDTNNKMVADSSGNLTIQAKSEDDRIWRIGYAENSFVEMMRVLLDDPGYTT"

for i in range(len(original_seq)):
    sequence[i].show()
    print("Pos: ", sequence[i].position, ", orig: ", original_seq[i], ", aa: ", sequence[i].aa)
