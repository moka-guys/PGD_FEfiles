'''
Created on 2 Oct 2015

@author: Aled
'''
import os
import fnmatch
# import numpy

# where the eve files are
embryo_control = "S:\\Genetics_Data2\\Array\\Audits and Projects\\150702 PGD FEfiles\\round8adele\\Embryo Control"
promega_control="S:\\Genetics_Data2\\Array\\Audits and Projects\\150702 PGD FEfiles\\round8adele\\Promega Control"
# count the number of files in this folder
number_of_files = len([name for name in os.listdir(embryo_control)])
n = 1
# loop through each filename in the folder
for afile in os.listdir(embryo_control):
    # open each file
    openfile = open(embryo_control + "\\" + afile)
    for i, line in enumerate(openfile):
        # pull out the stats line
        if i == 6:
            # split line and get the DLRS
            line = line.split('\t')
            embryo_control_DLRS = line[118]
        else:
            pass
    if int(afile[21]) == 5:
        tomatch = "3"
    elif int(afile[21]) == 3:
        tomatch = "5"
     
    # get substring for barcode and subarray_text (1_1)
    name_2_match_1 = afile[0:21]
    name_2_match_2 = afile[22:]
 
    # open a file to record the output
    output_file = open("S:\\Genetics_Data2\\Array\\Audits and Projects\\150702 PGD FEfiles\\round8adele\\DLRS_Comparison.txt", 'a+')
 
    # create a string to match to the original file name
    file_to_match = name_2_match_1 + tomatch + name_2_match_2
 
    # loop through the files in this folder, if they match the pattern from one of the eve files
    for file_b in os.listdir(promega_control):
        if fnmatch.fnmatch(file_b, file_to_match):
            # open and extract the DLRS
            open_original_file = open(promega_control + "\\" + file_b)
            for j, aline in enumerate(open_original_file):
                if j == 6:
                    aline = aline.split('\t')
                    promega_control_DLRS = aline[118]
                    # write the file name, original DLRS, EvE DLRS and the difference to the output file
                    output_file.write("Embryo control:\t"+str(afile) + "\t" + str(embryo_control_DLRS) + "\t Promega control:\t" + str(file_b) + "\t" + str(float(promega_control_DLRS)) +"\t Embryo_control-Promega_cotrol \t"+ str(float(embryo_control_DLRS)-float(promega_control_DLRS))+"\n")
                else:
                    pass
        else:
            pass
    # print the progress
    print "done file " + str(n) + " of " + str(number_of_files)
    n = n + 1
 
    # close file
    output_file.close()
