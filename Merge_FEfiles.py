'''
Created on 26 Jun 2015

@author: Aled
'''
import sys
import math
import numpy
import os
import fnmatch

class Merge_FEfile():
    ''' Usage: python create_dict_of_2_files.py file1,file1_dye,file2,file2_dye 
    File$ and File$_Dye specifies which samples (dye) you would like to combine
    This program creates a new FE file from these two samples. 
    NB The DLRS is recalculated but this calculation does not produce the same as what is produced during feature extraction 
    The output file is names file1_file1dye_file2_file2dye.txt'''
    
    #specify the input files
    chosenfolder="F:\\PGD_FE\\"#USB
    

    #name output file
    outputfolder="F:\\PGD_FE_OUTPUT\\"#USB
    
    # create dictionaries for features
    file1_dict={}
    file2_dict={}

    #some lists that are populated below 
    array1=[] # holds chrom, start and log ratio from non control probes
    sortedarray=[] # array1 but sorted on genomic location
    log_dict={} # a dictionary with key = chrom, value = a list of log ratios for that chrom 
    all_derivatives=[] # a list of all the calculated derivatives
    filtered_derivatives=[] # derivatives in the middle quartile
    
    file1=''
    file2=''
    file1_dye=''
    file2_dye=''
    outputfile=''
    outputfilename=''
    tempoutputfilename=''
    tempoutputfile=''
    
    files_to_find=[]
    list_of_files=[]

    def read_input_list(self):
        file2open = open("F:\\PGD_FE\\round2\\eve_input.txt",'r')
        for line in file2open:
            print line
            splitline=line.split('\t')
            file1_barcode=splitline[0]
            file1_subarray=int(splitline[1])
            file1_dye=splitline[2]
            file2_barcode=splitline[3]
            file2_subarray=int(splitline[4])
            file2_dye=splitline[5].rstrip()        

               
            if file1_subarray == 1:
                #assign to subarray the desired end to the filename. use ? as wildcard character
                file1_subarray="1_1.txt"
            elif file1_subarray == 2:
                file1_subarray="1_2.txt"
            elif file1_subarray == 3:
                file1_subarray="1_3.txt"
            elif file1_subarray== 4:
                file1_subarray="1_4.txt"
            elif file1_subarray== 5:
                file1_subarray="2_1.txt"
            elif file1_subarray == 6:
                file1_subarray="2_2.txt"
            elif file1_subarray == 7:
                file1_subarray="2_3.txt"
            elif file1_subarray == 8:
                file1_subarray="2_4.txt"
            else:
                print "error in file 1 subarray"
                
            if file2_subarray == 1:
                #assign to subarray the desired end to the filename. use ? as wildcard character
                file2_subarray="1_1.txt"
            elif file2_subarray == 2:
                file2_subarray="1_2.txt"
            elif file2_subarray == 3:
                file2_subarray="1_3.txt"
            elif file2_subarray== 4:
                file2_subarray="1_4.txt"
            elif file2_subarray== 5:
                file2_subarray="2_1.txt"
            elif file2_subarray == 6:
                file2_subarray="2_2.txt"
            elif file2_subarray == 7:
                file2_subarray="2_3.txt"
            elif file2_subarray == 8:
                file2_subarray="2_4.txt"
            else:
                print "error in subarray"
            
            filename1=str(file1_barcode)+"*"+file1_subarray
            filename2=str(file2_barcode)+"*"+file2_subarray
            
            self.files_to_find.append((filename1,file1_dye,filename2,file2_dye))
            
    def read_file(self):
        for i in self.files_to_find:
            file1_pattern=i[0]
            file1_dye=i[1]
            file2_pattern=i[2]
            file2_dye=i[3]
            
            for files in os.walk(self.chosenfolder):
                for name in files:
                    if fnmatch.fnmatch(name, file1_pattern):
                        file1_filename=name
                    else:
                        print "file not found"+file1_pattern
                    
                    if fnmatch.fnmatch(name, file2_pattern):
                        file2_filename=name
                    else:
                        print "file not found"+file2_pattern
            self.list_of_files.append((file1_filename,file1_dye,file2_filename,file2_dye))
                    
            
    
#     def get_sys_argvs(self,file1_in,dye1_in,file2_in,dye2_in):
#         '''capture the arguments'''
#         #capture variables from cmd line
#         self.file1=file1_in
#         self.file2=file2_in
#         self.file1_dye=dye1_in
#         self.file2_dye=dye2_in      
#     
#          
#     def create_dicts (self):
#         '''open files, create the temporary file and add features to dictionaries '''        
#         #open files
#         file1_open=open(self.chosenfolder+self.file1,'r')
#         file2_open=open(self.chosenfolder+self.file2,'r')
#          
#          
#         # create and open output file (remove .txt extension from filenames)
#         pre_output1=self.file1.replace("_S01_Guys121919_CGH_1100_Jul11",'')
#         pre_output2=self.file2.replace("_S01_Guys121919_CGH_1100_Jul11",'')
#         self.outputfilename=pre_output1.replace(".txt", '')+"_"+self.file1_dye+"_"+pre_output2.replace(".txt", '')+"_"+self.file2_dye+".txt"
#         self.tempoutputfilename=self.outputfilename.replace(".txt", '')+"temp.txt"
#         self.tempoutputfile=open(self.outputfolder+self.tempoutputfilename,'w')
#           
#         # open the first file and write first 10 lines (stats, feparams) to the output file.
#         for i, line in enumerate (file1_open):
#             if i < 10:
#                 self.tempoutputfile.write(line)
#             #then add the features to a dictionary, with the feature number as a key
#             if i >= 10:
#                 splitline=line.split('\t')
#                 self.file1_dict[int(splitline[1])] = line
#           
#         #repeat for features in second file
#         for i, line in enumerate(file2_open):
#             if i>=10:
#                 splitline=line.split('\t')
#                 self.file2_dict[int(splitline[1])] = line
#           
#         #close files
#         file1_open.close()
#         file2_open.close()
#       
#     def rewrite_file(self):
#         '''extract the desired sample(dye) from the dictionaries and re-write the fefile'''
#           
#         # get the specified dye for each file
#         if str(self.file1_dye) in ("cy3","Cy3") and str(self.file2_dye) in ("cy3","Cy3"):
#               
#             #Sort the dictionary on the keys so the file is in order of feature number. remove newline
#             for i in sorted(self.file1_dict.keys()):
#                 file1_line=self.file1_dict[i].rstrip()
#                 #for each feature split the line on tab and assign to f1 
#                 f1=file1_line.split('\t')
#                 #pull out the corresponding feature from file 2, split and assign to f2 
#                 file2_line=self.file2_dict[i].rstrip()
#                 f2=file2_line.split('\t')
#                   
#                 #Variables used to concatenate the line to write to file
#                 t="\t" # join
#                 logratio=math.log(float(f2[13])/float(f1[13]),10) # calculate the log ratio
#                 logratioerr=str(0)
#                 pval=str(0)
#                   
#                 #concatenate all the columns as required depending on the dyes selected. NB use of same f1 and f2 columns as the dyes are the same! 
#                 to_write=f1[0]+t+f1[1]+t+f1[2]+t+f1[3]+t+f1[4]+t+f1[5]+t+f1[6]+t+f1[7]+t+f1[8]+t+f1[9]+t+str(logratio)+t+logratioerr+t+pval+t+f1[13]+t+f2[13]+t+f1[15]+t+f2[15]+t+f1[17]+t+f2[17]+t+f1[19]+t+f2[19]+t+f1[21]+t+f2[21]+t+f1[23]+t+f2[23]+t+f1[25]+t+f2[25]+t+f1[27]+t+f2[27]+t+f1[29]+t+f2[29]+t+f1[31]+t+f2[31]+t+f1[33]+t+f1[34]+t+f2[34]+t+f1[36]+t+f2[36]+t+f1[38]+t+f2[38]+t+f1[40]+t+f1[41]+t+f2[41]+"\n"
#                  
#                 #write this to the temporary output file
#                 self.tempoutputfile.write(to_write)       
#           
#         # repeat for all combinations of dye      
#           
#         if str(self.file1_dye) in ("cy3","Cy3") and str(self.file2_dye) in ("cy5","Cy5"):
#             for i in sorted(self.file1_dict.keys()):
#                 file1_line=self.file1_dict[i].rstrip()
#                 f1=file1_line.split('\t')
#                   
#                 file2_line=self.file2_dict[i].rstrip()
#                 f2=file2_line.split('\t')
#                 t="\t"
#                 logratio=math.log(float(f2[14])/float(f1[13]),10)
#                 logratioerr=str(0)
#                 pval=str(0)
#                 # note different columns from f1+f2 selected as different dyes  
#                 to_write=f1[0]+t+f1[1]+t+f1[2]+t+f1[3]+t+f1[4]+t+f1[5]+t+f1[6]+t+f1[7]+t+f1[8]+t+f1[9]+t+str(logratio)+t+logratioerr+t+pval+t+f1[13]+t+f2[14]+t+f1[15]+t+f2[16]+t+f1[17]+t+f2[18]+t+f1[19]+t+f2[20]+t+f1[21]+t+f2[22]+t+f1[23]+t+f2[24]+t+f1[25]+t+f2[26]+t+f1[27]+t+f2[28]+t+f1[29]+t+f2[30]+t+f1[31]+t+f2[32]+t+f1[33]+t+f1[34]+t+f2[35]+t+f1[36]+t+f2[37]+t+f1[38]+t+f2[39]+t+f1[40]+t+f1[41]+t+f2[42]+"\n"
#                 self.tempoutputfile.write(to_write)
#                      
#         if str(self.file1_dye) in ("cy5","Cy5") and str(self.file2_dye) in ("cy3","Cy3"):
#             for i in sorted(self.file1_dict.keys()):
#                 file1_line=self.file1_dict[i].rstrip()
#                 f1=file1_line.split('\t')
#                   
#                 file2_line=self.file2_dict[i].rstrip()
#                 f2=file2_line.split('\t')
#                 t="\t"
#                 logratio=math.log(float(f2[13])/float(f1[14]),10)
#                 logratioerr=str(0)
#                 pval=str(0)
#                 to_write=f1[0]+t+f1[1]+t+f1[2]+t+f1[3]+t+f1[4]+t+f1[5]+t+f1[6]+t+f1[7]+t+f1[8]+t+f1[9]+t+str(logratio)+t+logratioerr+t+pval+t+f1[14]+t+f2[13]+t+f1[16]+t+f2[15]+t+f1[18]+t+f2[17]+t+f1[20]+t+f2[19]+t+f1[22]+t+f2[21]+t+f1[24]+t+f2[23]+t+f1[26]+t+f2[25]+t+f1[28]+t+f2[27]+t+f1[30]+t+f2[29]+t+f1[32]+t+f2[31]+t+f1[33]+t+f1[35]+t+f2[34]+t+f1[37]+t+f2[36]+t+f1[39]+t+f2[38]+t+f1[40]+t+f1[42]+t+f2[41]+"\n"
#                 self.tempoutputfile.write(to_write)    
#                   
#         if self.file1_dye in ("cy5","Cy5") and self.file2_dye in ("cy5","Cy5"):
#             for i in sorted(self.file1_dict.keys()):
#                 file1_line=self.file1_dict[i].rstrip()
#                 f1=file1_line.split('\t')
#                   
#                 file2_line=self.file2_dict[i].rstrip()
#                 f2=file2_line.split('\t')
#                 t="\t"
#                 logratio=math.log(float(f2[14])/float(f1[14]),10)
#                 logratioerr=str(0)
#                 pval=str(0)
#                 to_write=f1[0]+t+f1[1]+t+f1[2]+t+f1[3]+t+f1[4]+t+f1[5]+t+f1[6]+t+f1[7]+t+f1[8]+t+f1[9]+t+str(logratio)+t+logratioerr+t+pval+t+f1[14]+t+f2[14]+t+f1[16]+t+f2[16]+t+f1[18]+t+f2[18]+t+f1[20]+t+f2[20]+t+f1[22]+t+f2[22]+t+f1[24]+t+f2[24]+t+f1[26]+t+f2[26]+t+f1[28]+t+f2[28]+t+f1[30]+t+f2[30]+t+f1[32]+t+f2[32]+t+f1[33]+t+f1[35]+t+f2[35]+t+f1[37]+t+f2[37]+t+f1[39]+t+f2[39]+t+f1[40]+t+f1[42]+t+f2[42]+"\n"
#                 self.tempoutputfile.write(to_write)   
#         #close temp file now it's written
#         self.tempoutputfile.close()
#       
#   
#       
#     def calculate_DLRS(self):
#         '''To calculate the DLRS the newly created temp file is read.
#         The chromosome, start and log ratio are added to a new array
#         This array is sorted on genomic coords.
#         Maintaining the order a list of log ratios for each chrom are added to a dictionary with chrom as the key.
#         For each chromosome the list is read and the previous log ratio is subtracted to create a list of derivatives (differences between probes) 
#         The interquartile ranges are calculated and only the middle 50% of derivatves are kept.
#         The SD of these derivatives is calculated
#         This is then put into the stats line and the final output file is created    
#         '''
#         #open tempoutput file as read only
#         outputfile2=open(self.outputfolder+self.tempoutputfilename,'r')
#         for i, line in enumerate(outputfile2):
#             #for all features:
#             if i >= 10:
#                 splitline=line.split('\t')
#                 # remove all control probes and check that there are the correct number of columns
#                 if int(splitline[5])==0 and len(splitline)==43:
#                     #split the genomic location into three new fields
#                     genloc=splitline[7]
#                     genloc=genloc.replace('chr','')
#                     splitgenloc=genloc.replace('-',':').split(':')
#                       
#                     #change X and Y to numerical
#                     splitgenloc[0]=splitgenloc[0].replace('X','23')
#                     splitgenloc[0]=splitgenloc[0].replace('Y','24')
#                       
#                     # insert the split genomic location into the line
#                     splitline.insert(8,int(splitgenloc[0]))
#                     splitline.insert(9,int(splitgenloc[1]))
#                     splitline.insert(10,int(splitgenloc[2]))
#                       
#                     #append to an array (chrom, start and logratio score)
#                     self.array1.append((splitline[8],splitline[9],splitline[13]))
#                 
#                 elif int(splitline[5])==0 and len(splitline)!=43:
#                     raise ValueError ("temp file feature length !=43")
#                 
#             else:
#                 pass        
#         outputfile2.close()
#         
# 
#         #sort the arrays so probes are in genomic order    
#         self.sortedarray=sorted(self.array1,key=lambda tup: tup[1])
#         self.sortedarray=sorted(self.sortedarray,key=lambda tup: tup[0])
#           
#           
#         #go through each chromosome in order, and pull out the log ratio scores from the array (these should be in order) and add to a list. Add this list to a dictionary with the key as chromosome number
#         for i in range(1,25):
#             list=[]
#             for k in self.sortedarray:
#                 if k[0]==i:
#                     #print k
#                     list.append(k[2]) 
#             self.log_dict[i]=list
#         
#         # self.log_dict is {(chrom: 'probe1 log score','probe 2 log score'...).(chrom2:'probe1 log score;,...)}
#           
#         # for each chromosome (i is the key (chrom))
#         for i in self.log_dict:
#             #how many probes are there
#             num_of_probes=len(self.log_dict[i])
#             # for that number of probes
#             for j in range(num_of_probes):
#                 #excluding the first probe (as there is no probe to subtract)
#                 if j > 1:
#                     #pull out log ratio and calculate the difference between that and the previous probe. subtract the previous one from this probe and append to a new list
#                     n=float(self.log_dict[i][j])-float(self.log_dict[i][j-1])
#                     self.all_derivatives.append(n)
#           
#         
#         #use numpy to get the 25 and 75 percentile
#         q75,q25=numpy.percentile(self.all_derivatives,[75,25])
#         for i in self.all_derivatives:
#             if q25< i <q75:
#                 self.filtered_derivatives.append(i)
#         #print "len of all_derivatives: "+str(len(self.all_derivatives))
#         #print "len of filtered SD: "+str(len(self.filtered_derivatives))
#           
#           
#           
#         #calculate the DLSR by calculating the SD of this list    
#         DLSR=numpy.std(self.filtered_derivatives)
#         sqrt2=numpy.sqrt(2)
#         DLSR_sqrt=numpy.divide(DLSR,sqrt2)
#            
#         #open the final output file
#         finaloutput=open(self.outputfolder+self.outputfilename,'w')
#         outputfile3=open(self.outputfolder+self.tempoutputfilename,'r')
#           
#         #loop through the temp file and print it to a new file
#         for i, line in enumerate(outputfile3):
#             if i != 6:
#                 finaloutput.write(line)
#             #except for line 7 which needs the DLSR updating
#             elif i ==6:
#                 splitline=line.split('\t')
#                 splitline[166]=str(DLSR_sqrt)
#                 to_add='\t'.join(splitline)
#                 finaloutput.write(to_add)
#         #print "file created"
#           
#         #close files
#         outputfile3.close()
#         finaloutput.close()
#           
#         os.remove(self.outputfolder+self.tempoutputfilename)
#           
#         # clear all varaiables
#         self.file1_dict.clear()
#         self.file2_dict.clear()
#         del self.filtered_derivatives[:]
#         del self.array1[:]
#         del self.sortedarray[:]
#         self.log_dict.clear() 
#         del self.all_derivatives[:]
#         del self.filtered_derivatives[:]
         




# array1="column_test1.txt"
# array2="column_test1.txt"
# # array3="256755910289_S01_Guys121919_CGH_1100_Jul11_2_1_3.txt"
# # array4="256755910289_S01_Guys121919_CGH_1100_Jul11_2_1_4.txt"
# # array5="256755910289_S01_Guys121919_CGH_1100_Jul11_2_2_1.txt"
# # array6="256755910289_S01_Guys121919_CGH_1100_Jul11_2_2_2.txt"
# # array7="256755910289_S01_Guys121919_CGH_1100_Jul11_2_2_3.txt"
# # array8="256755910289_S01_Guys121919_CGH_1100_Jul11_2_2_4.txt"
# 
# 
# # this list may be specific to a single array slide. array 5 had a promega male v promega female. each sample on array 1-4 was compared to each of these = 16 files.
# #Then each sample on arrays 6-8 were paired together (12 new files).   
# #mylist=[(array1,'cy3',array5,'cy3'),(array1,'cy3',array5,'cy5'),(array1,'cy5',array5,'cy3'),(array1,'cy5',array5,'cy5'),(array2,'cy3',array5,'cy3'),(array2,'cy3',array5,'cy5'),(array2,'cy5',array5,'cy3'),(array2,'cy5',array5,'cy5'),(array3,'cy3',array5,'cy3'),(array3,'cy3',array5,'cy5'),(array3,'cy5',array5,'cy3'),(array3,'cy5',array5,'cy5'),(array4,'cy3',array5,'cy3'),(array4,'cy3',array5,'cy5'),(array4,'cy5',array5,'cy3'),(array4,'cy5',array5,'cy5'),(array6,'cy3',array7,'cy3'),(array6,'cy3',array7,'cy5'),(array6,'cy3',array8,'cy3'),(array6,'cy3',array8,'cy5'),(array6,'cy5',array7,'cy3'),(array6,'cy5',array7,'cy5'),(array6,'cy5',array8,'cy3'),(array6,'cy5',array8,'cy5'),(array7,'cy3',array8,'cy3'),(array7,'cy3',array8,'cy5'),(array7,'cy5',array8,'cy3'),(array7,'cy5',array8,'cy5')]
# #mylist=[(array1,'cy3',array2,'cy3'),(array1,'cy5',array2,'cy3'),(array1,'cy3',array2,'cy5'),(array1,'cy5',array2,'cy5')]#,(array,'cy3',array5,'cy3'),(array7,'cy5',array5,'cy3'),(array7,'cy3',array5,'cy5'),(array7,'cy5',array5,'cy5'),(array8,'cy3',array5,'cy3'),(array8,'cy5',array5,'cy3'),(array8,'cy3',array5,'cy5'),(array8,'cy5',array5,'cy5')]
# mylist=[(array1,'cy3',array2,'cy5')]


n=1

a=Merge_FEfile()    
a.read_input_list()
# for i in Merge_FEfile.list_of_files:
#     print i  
#     file_in_1=i[0]
#     file_in_2=i[2]
#     file_in_1_dye=i[1]
#     file_in_2_dye=i[3]  

    #instance of the class
    
    #a.get_sys_argvs(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
#     a.get_sys_argvs(file_in_1,file_in_1_dye,file_in_2,file_in_2_dye)
#     a.create_dicts()
#     a.rewrite_file()
#     a.calculate_DLRS()
#     print "done file "+str(n)+" of "+str(len(mylist))
#     n=n+1
