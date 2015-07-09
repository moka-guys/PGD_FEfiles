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
from decimal import *

folder="F:\\PGD_FE\\Col_Testing\\output"
for filename in os.listdir(folder):
    #print filename
    #print "FEfile created = "+filename.replace('_S01_1_1_',' ')
    fname=filename.replace('_S01_1_1_','_')
    fname=fname.replace('.txt','')
    fname=fname.replace('_F',' F')
    fname=fname.lower()
#     print fname
    
    fefile=open(folder+"\\"+filename)
    for i, line in enumerate(fefile):
        if i == 15:
            linesplit=line.split('\t')
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

            assert processedsignal==ProcessedSigError and ProcessedSigError==MedianSignal and ProcessedSigError==BGMedianSignal and ProcessedSigError==BGPixSDev and ProcessedSigError==IsSaturated and ProcessedSigError==IsFeatNonUnifOL and ProcessedSigError==IsBGNonUnifOL and ProcessedSigError==IsFeatPopnOL and ProcessedSigError==IsBGPopnOL and ProcessedSigError==BGSubSignal and ProcessedSigError==IsPosAndSignif and ProcessedSigError==IsWellAboveBG and ProcessedSigError==BGMeanSignal
            
            list_of_results=[("file1_cy3 file1_cy3",1),("file1_cy3 file1_cy5",0.25),("file1_cy3 file2_cy3",0.2),("file1_cy3 file2_cy5",0.02),("file1_cy5 file1_cy3",16),("file1_cy5 file1_cy5",4),("file1_cy5 file2_cy3",3.2),("file1_cy5 file2_cy5",.32),("file2_cy3 file1_cy3",25),("file2_cy3 file1_cy5",6.25),("file2_cy3 file2_cy3",5),("file2_cy3 file2_cy5",0.5),("file2_cy5 file1_cy3",2500),("file2_cy5 file1_cy5",625),("file2_cy5 file2_cy3",500),("file2_cy5 file2_cy5",50)]
            #print processedsignal
            for i in list_of_results:
                if i[1]==processedsignal:
#                     print i[0]
#                     print fname
#                     print "the combination of files and dyes used must have been "+i[0]
                    assert str(i[0])==fname
                else:
                    pass
                    #print "error"+str(processedsignal) 

            logratio=round(float(linesplit[10]),8)
            
            check_log_ratio=round(float(math.log(float(rProcessedSignal)/float(gProcessedSignal),10)),8)
            assert logratio == check_log_ratio
            #print "original logratio "+str(logratio)+" check = "+str(check_log_ratio)+"\n"
print "Files match as expected"