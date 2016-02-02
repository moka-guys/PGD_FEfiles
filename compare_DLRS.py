'''
This script was used to compare the DLRS of 800 FE files which were recreated using EvE.
The exact same pairing was used as the original hyb so the only difference is the DLRS.
Therefore below the barcode and subarray is captured from the cy3 barcode to identify the original FE file as cy3 and cy5 are the same!
In the future to compare a patient hyb'd against multiple control samples the selection of barcode and subarray will need changing.
'''
import os
import fnmatch
import numpy

# where the eve files are
eve_output="S:\\Genetics_Data2\\Array\\Audits and Projects\\150702 PGD FEfiles\\aled_DLRS\\EvE_output"
# count the number of files in this folder
number_of_files=len([name for name in os.listdir(eve_output)])
n=1
# loop through each filename in the folder
for file in os.listdir(eve_output):
    #open each file
    openfile=open(eve_output+"\\"+file)
    for i, line in enumerate(openfile):
        #pull out the stats line
        if i == 6:
            #split line and get the DLRS
            line=line.split('\t')
            eve_DLRS=line[118]
        else:
            pass
    #get substring for barcode and subarray_text (1_1)
    # see docstring. the cy5 barcode may need to be captured from eve filename to find the original.
    barcode=file[0:12]
    subarray_text=file[15:18]
    
    #open a file to record the output
    output_file=open("S:\\Genetics_Data2\\Array\\Audits and Projects\\150702 PGD FEfiles\\aled_DLRS\\800_DLRS_comparison.txt",'a+')
    
    #create a string to match to the original file name
    file_to_match=str(barcode) + "_S01*" + str(subarray_text)+".txt"
    
    #FE folder containing original files
    FEfiles="S:\\Genetics_Data2\\Array\\FeatureExtraction"
    
    #loop through the files in this folder, if they match the pattern from one of the eve files
    for afile in os.listdir(FEfiles):
        if fnmatch.fnmatch(afile, file_to_match):
            #open and extract the DLRS
            open_original_file=open(FEfiles+"\\"+afile)
            for j, aline in enumerate(open_original_file):
                if j == 6:
                    aline=aline.split('\t')
                    original_DLRS=aline[118]
                    #write the file name, original DLRS, EvE DLRS and the difference to the output file
                    output_file.write(str(file) + "\t EVE_DLRS \t"+str(eve_DLRS)+"\t original_DLRS \t"+str(original_DLRS)+"\t eve-original \t"+str(float(eve_DLRS)-float(original_DLRS))+"\n")
                else:
                    pass
        else:
            pass
    # print the progress
    print "done file "+str(n)+" of " + str(number_of_files)
    n=n+1
    
output_file.seek(0)
eve=[]
original=[]
for k in output_file:
    split=k.split("\t")
    eve.append(float(split[2]))
    original.append(float(split[4]))

eve_std=numpy.std(eve)
eve_mean=numpy.mean()
orig_std=numpy.std(original)
orig_mean=numpy.mean(original)

output_file.write("original_mean \t"+str(orig_mean))
output_file.write("\n original_STD \t"+str(orig_std))
output_file.write("\n original sample size \t"+str(len(original)+"\n"))
output_file.write("\n eve_mean \t"+str(eve_mean))
output_file.write("\n eve_STD \t"+str(eve_std))
output_file.write("\n eve_sample size \t"+str(len(eve)))

# close file
output_file.close()

