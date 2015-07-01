'''
Created on 26 Jun 2015

@author: Aled
'''
import sys
import math
import numpy
import os

class Merge_FEfile():
    #specify the input files
    chosenfolder="F:\\fefiles\\"#USB

    #name output file
    outputfolder="F:\\fefiles\\"#USB
    
    
    # create dictionaries for features
    file1_dict={}
    file2_dict={}

    def get_sys_argvs(self,file1_in,dye1_in,file2_in,dye2_in):
        # name global variables
        global file1
        global file2
        global file1_dye
        global file2_dye
        #capture variables from cmd line
        file1=file1_in
        file2=file2_in
        file1_dye=dye1_in
        file2_dye=dye2_in
       
#     def print_globals(self):
#         print file1
#         print file1_dye
#         print file2
#         print file2_dye
        
    def create_dicts (self):
        #global variables
        global outputfile
        global outputfilename
        global tempoutputfilename
        global tempoutputfile
        
        # open files
        file1_open=open(self.chosenfolder+file1,'r')
        file2_open=open(self.chosenfolder+file2,'r')
        
        # create and open output file
        outputfilename=file1+"_"+file2
        tempoutputfilename="temp.txt"
        tempoutputfile=open(self.outputfolder+tempoutputfilename,'w')
        
        # open the first file and write first 10 lines to the output file.
        for i, line in enumerate (file1_open):
            if i < 10:
                tempoutputfile.write(line)
            #then add the features to a dictionary, with the feature number as a key
            if i >= 10:
                splitline=line.split('\t')
                self.file1_dict[int(splitline[1])] = line
        
        #repeat for features in second file
        for i, line in enumerate(file2_open):
            if i>=10:
                splitline=line.split('\t')
                self.file2_dict[int(splitline[1])] = line
        
        #close files
        file1_open.close()
        file2_open.close()
    
    def rewrite_file(self):
        # get the dye for each file
        if str(file1_dye) in ("cy3","Cy3") and str(file2_dye) in ("cy3","Cy3"):
            #then sort the dictionary on the keys so the file is in order of feature number
            for i in sorted(self.file1_dict.keys()):
                file1_line=self.file1_dict[i].rstrip()
                #for each feature split the line and assign to f1 
                f1=file1_line.split('\t')
                #pull out the corresponding feature from file 2, split and assign to f2 
                file2_line=self.file2_dict[i].rstrip()
                f2=file2_line.split('\t')
                
                #Variables used to concatenate the line to write to file
                t="\t" # join
                logratio=math.log(float(f2[13])/float(f1[13]),2) # calculate the log ratio
                logratioerr=str(0)
                pval=str(0)
                #concatenate all the columns as required depending on the dyes selected
                to_write=f1[0]+t+f1[1]+t+f1[2]+t+f1[3]+t+f1[4]+t+f1[5]+t+f1[6]+t+f1[7]+t+f1[8]+t+f1[9]+t+str(logratio)+t+logratioerr+t+pval+t+f1[13]+t+f2[13]+t+f1[15]+t+f2[15]+t+f1[17]+t+f2[17]+t+f1[19]+t+f2[19]+t+f1[21]+t+f2[21]+t+f1[23]+t+f2[23]+t+f1[25]+t+f2[25]+t+f1[27]+t+f2[27]+t+f1[29]+t+f2[29]+t+f1[31]+t+f2[31]+t+f1[33]+t+f1[34]+t+f2[34]+t+f1[36]+t+f2[36]+t+f1[38]+t+f2[38]+t+f1[40]+t+f1[41]+t+f2[41]+"\n"
                #print to_write
                tempoutputfile.write(to_write)       
        
        # repeat for all combinations of dye      
        if str(file1_dye) in ("cy3","Cy3") and str(file2_dye) in ("cy5","Cy5"):
            for i in sorted(self.file1_dict.keys()):
                file1_line=self.file1_dict[i].rstrip()
                f1=file1_line.split('\t')
                
                file2_line=self.file2_dict[i].rstrip()
                f2=file2_line.split('\t')
                t="\t"
                print str(f1[1])+" "+str(f1[13])+" "+str(f2[14])
                logratio=math.log(float(f2[14])/float(f1[13]),2)
                logratioerr=str(0)
                pval=str(0)
                to_write=f1[0]+t+f1[1]+t+f1[2]+t+f1[3]+t+f1[4]+t+f1[5]+t+f1[6]+t+f1[7]+t+f1[8]+t+f1[9]+t+str(logratio)+t+logratioerr+t+pval+t+f1[13]+t+f2[14]+t+f1[15]+t+f2[16]+t+f1[17]+t+f2[18]+t+f1[19]+t+f2[20]+t+f1[21]+t+f2[22]+t+f1[23]+t+f2[24]+t+f1[25]+t+f2[26]+t+f1[27]+t+f2[28]+t+f1[29]+t+f2[30]+t+f1[31]+t+f2[32]+t+f1[33]+t+f1[34]+t+f2[35]+t+f1[36]+t+f2[37]+t+f1[38]+t+f2[39]+t+f1[40]+t+f1[41]+t+f2[42]+"\n"
                #print to_write
                tempoutputfile.write(to_write)
                   
        if str(file1_dye) in ("cy5","Cy5") and str(file2_dye) in ("cy3","Cy3"):
            for i in sorted(self.file1_dict.keys()):
                file1_line=self.file1_dict[i].rstrip()
                f1=file1_line.split('\t')
                
                file2_line=self.file2_dict[i].rstrip()
                f2=file2_line.split('\t')
                t="\t"
                logratio=math.log(float(f2[13])/float(f1[14]),2)
                logratioerr=str(0)
                pval=str(0)
                to_write=f1[0]+t+f1[1]+t+f1[2]+t+f1[3]+t+f1[4]+t+f1[5]+t+f1[6]+t+f1[7]+t+f1[8]+t+f1[9]+t+str(logratio)+t+logratioerr+t+pval+t+f1[14]+t+f2[13]+t+f1[16]+t+f2[15]+t+f1[18]+t+f2[17]+t+f1[20]+t+f2[19]+t+f1[22]+t+f2[21]+t+f1[24]+t+f2[23]+t+f1[26]+t+f2[25]+t+f1[28]+t+f2[27]+t+f1[30]+t+f2[29]+t+f1[32]+t+f2[31]+t+f1[33]+t+f1[35]+t+f2[34]+t+f1[37]+t+f2[36]+t+f1[39]+t+f2[38]+t+f1[40]+t+f1[42]+t+f2[41]+"\n"
                #print to_write
                tempoutputfile.write(to_write)    
                
        if file1_dye in ("cy5","Cy5") and file2_dye in ("cy5","Cy5"):
            for i in sorted(self.file1_dict.keys()):
                file1_line=self.file1_dict[i].rstrip()
                f1=file1_line.split('\t')
                
                file2_line=self.file2_dict[i].rstrip()
                f2=file2_line.split('\t')
                t="\t"
                #print str(f1[13])+" "+str(f2[14])
                
                logratio=math.log(float(f2[14])/float(f1[14]),2)
                logratioerr=str(0)
                pval=str(0)
                to_write=f1[0]+t+f1[1]+t+f1[2]+t+f1[3]+t+f1[4]+t+f1[5]+t+f1[6]+t+f1[7]+t+f1[8]+t+f1[9]+t+str(logratio)+t+logratioerr+t+pval+t+f1[14]+t+f2[14]+t+f1[16]+t+f2[16]+t+f1[18]+t+f2[18]+t+f1[20]+t+f2[20]+t+f1[22]+t+f2[22]+t+f1[24]+t+f2[24]+t+f1[26]+t+f2[26]+t+f1[28]+t+f2[28]+t+f1[30]+t+f2[30]+t+f1[32]+t+f2[32]+t+f1[33]+t+f1[35]+t+f2[35]+t+f1[37]+t+f2[37]+t+f1[39]+t+f2[39]+t+f1[40]+t+f1[42]+t+f2[42]+"\n"
                #print to_write
                tempoutputfile.write(to_write)   
        tempoutputfile.close()
    
    #some lists populate below 
    array1=[] # holds chrom, start and log ratio from non control probes
    sortedarray=[] # array1 but sorted on genomic location
    log_dict={} # a dictionary with key = chrom, value = a list of log ratios for that chrom 
    all_derivatives=[] # a list of all the calc ulated derivatives
    filtered_derivatives=[] # derivatives in the middle quartile
    
    def calculate_DLRS(self):
        #open tempoutput file as read only
        outputfile2=open(self.outputfolder+tempoutputfilename,'r')
        for i, line in enumerate(outputfile2):
            #for all features:
            if i >= 10:
                splitline=line.split('\t')
                # remove all control probes and check that there are the correct number of columns
                if int(splitline[5])==0 and len(splitline)==43:
                    #split the genomic location into three new fields
                    genloc=splitline[7]
                    genloc=genloc.replace('chr','')
                    splitgenloc=genloc.replace('-',':').split(':')
                    #change X and Y to numerical
                    splitgenloc[0]=splitgenloc[0].replace('X','23')
                    splitgenloc[0]=splitgenloc[0].replace('Y','24')
                    splitline.insert(8,int(splitgenloc[0]))
                    splitline.insert(9,int(splitgenloc[1]))
                    splitline.insert(10,int(splitgenloc[2]))
                    #append to an array (chrom, start and logratio score)
                    self.array1.append((splitline[8],splitline[9],splitline[13]))
                else:
                    if int(splitline[5])==0:
                        #print any NON-control probes that do not have correct length
                        print splitline
            else:
                pass        
        outputfile2.close()
                
        #sort the arrays so probes are in genomic order    
        self.sortedarray=sorted(self.array1,key=lambda tup: tup[1])
        self.sortedarray=sorted(self.sortedarray,key=lambda tup: tup[0])
        
        
        #go through each chromosome in order, and pull out the log ratio scores from the array (these should be in order) and add to a list. Add this list to a dictionary with the key as chromosome number
        for i in range(1,25):
            list=[]
            for k in self.sortedarray:
                if k[0]==i:
                    print k
                    list.append(k[2]) #### MAKE SURE THIS IS MAINTAINING ORDER
            self.log_dict[i]=list
        
        # for each chromosome
        for i in self.log_dict:
            #how many probes are there
            num_of_probes=len(self.log_dict[i])
            # for that number of probes
            for j in range(num_of_probes):
                #excluding the first one
                if j > 1:
                    #pull out log ratio and calculate the difference between that and the previous probe. subtract the previous one from this probe and append to a new list
                    n=float(self.log_dict[i][j])-float(self.log_dict[i][j-1])###MAKE SURE THIS IS MAINTAINING THE ORDER
                    self.all_derivatives.append(n)
        
#         #use numpy to get the 25 and 75 percentile
#         q75,q25=numpy.percentile(self.all_derivatives,[75,25])
#         for i in self.all_derivatives:
#             if q25< i <q75:
#                 self.filtered_derivatives.append(i)
#         #print "len of all_derivatives: "+str(len(self.all_derivatives))
#         #print "len of filtered SD: "+str(len(self.filtered_derivatives))
        
        #calculate the DLSR by calculating the SD of this list    
        DLSR=numpy.std(self.all_derivatives)
        print "DLSR = "+str(DLSR)
         
        #open the final output file
        finaloutput=open(self.outputfolder+outputfilename,'w')
        outputfile3=open(self.outputfolder+tempoutputfilename,'r')
        
        #loop through the temp file and print it to a new file
        for i, line in enumerate(outputfile3):
            if i != 6:
                finaloutput.write(line)
            #except for line 7 which needs the DLSR updating
            elif i ==6:
                #print line
                splitline=line.split('\t')
                sqrt2=numpy.sqrt(2)
                splitline[166]=str(numpy.divide(DLSR,sqrt2))
                print "DLRS/sqrt(2) = "+str(numpy.divide(DLSR,sqrt2)) 
                #print splitline[166]
                to_add='\t'.join(splitline)
                finaloutput.write(to_add)
        print "file created"
        
        #close files
        outputfile3.close()
        finaloutput.close()
        
        #os.remove(self.outputfolder+tempoutputfilename)
        
file1="example1.txt"
file2=file1
file1_dye="cy3"
file2_dye="cy5"
#Merge_FEfile().get_sys_argvs(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
Merge_FEfile().get_sys_argvs(file1,file1_dye,file2,file2_dye)
Merge_FEfile().create_dicts()
Merge_FEfile().rewrite_file()
Merge_FEfile().calculate_DLRS()


