import os
import fnmatch

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
    barcode=file[0:12]
    subarray_text=file[15:18]
    
    #open a file to record the output
    output_file=open("S:\\Genetics_Data2\\Array\\Audits and Projects\\150702 PGD FEfiles\\aled_DLRS\\DLRS_comparison.txt",'a')
    
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
# close file
output_file.close()