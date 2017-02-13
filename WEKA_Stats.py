import sys
import re
import os 
from subprocess import call
from shutil import copyfile

# python 3.4.py 20000.TRAINING.some.arff
if __name__ == '__main__':
    os.system("rm -r 3.4/*.arff")
    file = sys.argv[1]
    f = open(file, "r")
    os.system('echo "3.4 Cross-validation" >> 3.4output.txt')
    os.system('echo "WEKA J40 -10 fold" >> 3.4output.txt')
    # build the 20000.arff file
    os.system('python buildarff.py TRAINING.test.twt 20000.TRAINING.some.arff 10000')
    # Create 10 partitions
    bins = []
    # create 10 bin files
    for i in range(1,11):
        binName = "3.4/bin_" + str(i) + ".arff"
        bins.append(binName)
        
    # add data to the bins
    c = 0
    for line in f:
        data = re.search("^[0-9]+", line)
        if data:
            of = open(bins[c], "a")
            of.write(line)
            of.close()
            c += 1
            if c == 10:
                c = 0
    # Concatenate all other partitions
    all_concatParti = []
    for _bin in bins:
        for _bin2 in bins:
            if _bin != _bin2:
                newFileName = _bin.split(".")
                concatParti = "3." + newFileName[1] + "_CP." + newFileName[-1]
                all_concatParti.append(concatParti)
                os.system("cat " + _bin2 + " >> " + concatParti)
                
    # add headers to concat'ed partitions and bins
    for cp in list(set(all_concatParti)):
        cp_name = cp.split("/")
        new_cp = cp_name[0] + "/GOLD_" + cp_name[-1]
        os.system("cat arff_header.txt >> " + new_cp)
        os.system("cat " + cp + " >> " + new_cp)
    for _bin in bins:
        bin_name = _bin.split("/")
        new_bin = bin_name[0] + "/GOLD_" + bin_name[-1]
        os.system("cat arff_header.txt >> " + new_bin)
        os.system("cat " + _bin + " >> " + new_bin)
    # for each partition get accuracy, precision, and recall
    # get accurarcy, precision and recall
    for j in range(1,11):
        os.system('echo "obtaining accurarcy for fold #'+str(j)+'" >> COMP_3.4output.txt')
        os.system('java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t 3.4/GOLD_bin_'+str(j)+'_CP.arff -T 3.4/GOLD_bin_'+str(j)+'.arff -v -o -i >> COMP_3.4output.txt')
                