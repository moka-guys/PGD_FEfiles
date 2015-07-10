'''
Created on 8 Jul 2015

@author: Aled
'''
#for each file in F:\PGD_FE\Col_Testing\output
#open and for one feature row:
#squre the cy 3 column and then divide by the cy5 column
#match the answer to the expected outcomes to predict which columns were used.
#also calculate the log ratio   

import os
import math
'''
This document tests that the FE files created using specific FE and input files are correct.
It ensures the correct columns are selected and that the log ratio is calculated correctly
file 1 cy3 values = 1
file 1 cy5 values = 4
file 2 cy3 values = 5
file 2 cy5 values = 20
The input file specifies all 16 combinations of these columns.
'''

#folder containing all the test FE files.
folder="F:\\PGD_FE\\Col_Testing\\output"

#for each file: 
for filename in os.listdir(folder):
    #remove strings and manipulate to replicate the names of the expected file outcomes "file1_dye file2_dye"
    fname=filename.replace('_S01_1_1_','_')
    fname=fname.replace('.txt','')
    fname=fname.replace('_F',' F')
    fname=fname.lower()

    #open the fe file    
    fefile=open(folder+"\\"+filename)
    # take a random row eg row 15
    for i, line in enumerate(fefile):
        if i == 15:
            #split on tab
            linesplit=line.split('\t')
            #capture each column
            gProcessedSignal=float(linesplit[13])
            rProcessedSignal=float(linesplit[14])
            gProcessedSigError=float(linesplit[15])
            rProcessedSigError=float(linesplit[16])
            gMedianSignal=float(linesplit[17])
            rMedianSignal=float(linesplit[18])
            gBGMedianSignal=float(linesplit[19])
            rBGMedianSignal=float(linesplit[20])
            gBGPixSDev=float(linesplit[21])
            rBGPixSDev=float(linesplit[22])
            gIsSaturated=float(linesplit[23])
            rIsSaturated=float(linesplit[24])
            gIsFeatNonUnifOL=float(linesplit[25])
            rIsFeatNonUnifOL=float(linesplit[26])
            gIsBGNonUnifOL=float(linesplit[27])
            rIsBGNonUnifOL=float(linesplit[28])
            gIsFeatPopnOL=float(linesplit[29])
            rIsFeatPopnOL=float(linesplit[30])
            gIsBGPopnOL=float(linesplit[31])
            rIsBGPopnOL=float(linesplit[32])
            gBGSubSignal=float(linesplit[34])
            rBGSubSignal=float(linesplit[35])
            gIsPosAndSignif=float(linesplit[36])
            rIsPosAndSignif=float(linesplit[37])
            gIsWellAboveBG=float(linesplit[38])
            rIsWellAboveBG=float(linesplit[39])
            gBGMeanSignal=float(linesplit[41])
            rBGMeanSignal=float(linesplit[42])
            
            # pair up the relevant columns and perform the calculation (cy3*cy3)/cy5
            processedsignal=(gProcessedSignal*gProcessedSignal)/rProcessedSignal
            ProcessedSigError=(gProcessedSigError*gProcessedSigError)/rProcessedSigError
            MedianSignal=(gMedianSignal*gMedianSignal)/rMedianSignal
            BGMedianSignal=(gBGMedianSignal*gBGMedianSignal)/rBGMedianSignal
            BGPixSDev=(gBGPixSDev*gBGPixSDev)/rBGPixSDev
            IsSaturated=(gIsSaturated*gIsSaturated)/rIsSaturated
            IsFeatNonUnifOL=(gIsFeatNonUnifOL*gIsFeatNonUnifOL)/rIsFeatNonUnifOL
            IsBGNonUnifOL=(gIsBGNonUnifOL*gIsBGNonUnifOL)/rIsBGNonUnifOL
            IsFeatPopnOL=(gIsFeatPopnOL*gIsFeatPopnOL)/rIsFeatPopnOL
            IsBGPopnOL=(gIsBGPopnOL*gIsBGPopnOL)/rIsBGPopnOL
            BGSubSignal=(gBGSubSignal*gBGSubSignal)/rBGSubSignal
            IsPosAndSignif=(gIsPosAndSignif*gIsPosAndSignif)/rIsPosAndSignif
            IsWellAboveBG=(gIsWellAboveBG*gIsWellAboveBG)/rIsWellAboveBG
            BGMeanSignal=(gBGMeanSignal*gBGMeanSignal)/rBGMeanSignal
            
            #assert that all columns produce the same result (that the correct columns have been selected across all columns)
            assert processedsignal==ProcessedSigError and ProcessedSigError==MedianSignal and ProcessedSigError==BGMedianSignal and ProcessedSigError==BGPixSDev and ProcessedSigError==IsSaturated and ProcessedSigError==IsFeatNonUnifOL and ProcessedSigError==IsBGNonUnifOL and ProcessedSigError==IsFeatPopnOL and ProcessedSigError==IsBGPopnOL and ProcessedSigError==BGSubSignal and ProcessedSigError==IsPosAndSignif and ProcessedSigError==IsWellAboveBG and ProcessedSigError==BGMeanSignal
            
            #A list of expected results for every combination of file and dye:
            list_of_results=[("file1_cy3 file1_cy3",1),("file1_cy3 file1_cy5",0.25),("file1_cy3 file2_cy3",0.2),("file1_cy3 file2_cy5",0.02),("file1_cy5 file1_cy3",16),("file1_cy5 file1_cy5",4),("file1_cy5 file2_cy3",3.2),("file1_cy5 file2_cy5",.32),("file2_cy3 file1_cy3",25),("file2_cy3 file1_cy5",6.25),("file2_cy3 file2_cy3",5),("file2_cy3 file2_cy5",0.5),("file2_cy5 file1_cy3",2500),("file2_cy5 file1_cy5",625),("file2_cy5 file2_cy3",500),("file2_cy5 file2_cy5",50)]
            
            # go through this list of results looking to see which combination of files and dyes must have been used to make this file based on the result of the (cy3*cy3)cy5 calculation  
            for i in list_of_results:
                if i[1]==processedsignal:
                    #assert that the file names are the same. no other combination of file/columns could produce that result and the output file name details which file/columns were used   
                    assert str(i[0])==fname
                else:
                    pass
                    #print "error"+str(processedsignal) 
            
            #===================================================================
            # Now the columns have been determined to be correct check the correct columns have been used to calculate log ratio
            # (the selection of columns to calculate the log ratio is seperate to the selection of cols to write the file)
            #===================================================================
            
            #get the log ratio from the FE file, round to 8dp
            logratio=round(float(linesplit[10]),8)
            
            #calculate the log ratio from the columns (now known to be the correct columns), rounded to 8dp 
            check_log_ratio=round(float(math.log(float(rProcessedSignal)/float(gProcessedSignal),10)),8)
            
            #assert that the value is correct
            assert logratio == check_log_ratio
            #print "original logratio "+str(logratio)+" check = "+str(check_log_ratio)+"\n"

print "If this is the only output then all files were produced correctly"