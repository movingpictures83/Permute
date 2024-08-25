import PyPluMA
import os
import random

class PermutePlugin:
    def input(self, infile):
        self.parameters = dict()
        myparam = open(infile, 'r')
        params = dict()
        for line in myparam:
            line = line.strip()
            contents = line.split('\t')
            params[contents[0]] = contents[1]
        csvfile = open(PyPluMA.prefix()+"/"+params["csvfile"], 'r')  # Data
        self.header = csvfile.readline()
        self.cols = []
        self.data = []
        for line in csvfile:
            line = line.strip()
            contents = line.split(',')
            self.cols.append(contents[0])
            for i in range(1, len(contents)):
                self.data.append(contents[i])
        self.outputdir = PyPluMA.prefix()+"/"+params["outputdir"] # Output directory for permutations
        if (not os.path.exists(self.outputdir)):
           os.makedirs(self.outputdir)
        self.numperms = int(params["numperms"])

    def run(self):
        # Permute self.data
        self.perms = []

        # Assemble array of indices
        indices = []
        for i in range(len(self.data)):
           indices.append(i)

        for i in range(self.numperms):
           random.shuffle(indices)
           self.perms.append([])
           for j in range(len(indices)):
               self.perms[i].append(self.data[indices[j]])

    def output(self, filename):
        #outputdir = prefix[:prefix.rfind("/")]
        #if (not os.path.exists(outputdir)):
        #   os.makedirs(outputdir)
        for i in range(self.numperms):
           outputdirperm = self.outputdir+"/"+str(i)
           if (not os.path.exists(outputdirperm)):
               os.makedirs(outputdirperm)
           #outputfile = open(prefix+"."+str(i)+".csv", 'w')
           outputfile = open(outputdirperm+"/"+filename[filename.rfind('/'):], 'w')
           outputfile.write(self.header)
           numperrow = len(self.header.strip().split(','))-1
           pos = 0
           for j in range(len(self.cols)):
               outputfile.write(self.cols[j]+",")
               for k in range(numperrow):
                   outputfile.write(self.perms[i][pos])
                   pos += 1
                   if (k != numperrow-1):
                       outputfile.write(',')
                   else:
                       outputfile.write('\n')
