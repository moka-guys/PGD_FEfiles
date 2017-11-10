'''
Updated 11/8/15

 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * aledjones@nhs.net wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return. Aled
 * ----------------------------------------------------------------------------
 
'''
import sys
import math
import numpy
import os
import fnmatch


class Merge_FEfile():
    '''
    Cmd line Usage: python EvE.py inputfile.txt output folder
    There is no need for a trailing / for the output folder

    input file is a tab delimited file in format:
    barcode 1    subarray    dye1    barcode 2    subarray    dye 2 filename_prefix(optional)

    This script finds the two FE file which matches this input and creates a new FE file from these two samples using the dyes specified.
    The log ratio is re calculated
    NB The DLRS is recalculated but this calculation does not produce the same as what is produced during feature extraction

    The output file is named (prefix is optional) prefix_file1_file1dye_file2_file2dye.txt
    '''
	def __init__(self):
		# where the FE files are REMEMBER TO END WITH \\
		# chosenfolder="I:\\PGD_FE\\Col_Testing\\"# column_test_USB
		# chosenfolder="I:\\PGD_FE\\"#USB non unit test
		self.chosenfolder = "S:\\Genetics_Data2\\Array\\FeatureExtraction\\"  # work network

		# when output folder is taken from command line argument:
		self.outputfolder = ''

		# if hard coded: REMEMBER TO END WITH \\
		# self.outputfolder="S:\\Genetics_Data2\\Array\\Audits and Projects\\150702 PGD FEfiles\\round 2\\output\\"#work network
		# self.outputfolder="F:\\PGD_FE\\Col_Testing\\output\\" #column_test_USB

		# create dictionaries for features
		self.file1_dict = {}
		self.file2_dict = {}

		# some lists that are populated below
		self.array1 = []  # holds chrom, start and log ratio from non control probes
		self.sortedarray = []  # self.array1 but sorted on genomic location
		self.log_dict = {}  # a dictionary with key = chrom, value = a list of log ratios for that chrom
		self.all_derivatives = []  # a list of all the calculated derivatives
		self.filtered_derivatives = []  # derivatives in the middle quartile
		self.files_to_find = []  # list of filename patterns to search for from text file
		self.list_of_files = []  # list of complete filenames and dyes from text file 
		self.report = [] # report


		# variables to be populated in get_sys_argv and create_dicts
		self.file1 = ''
		self.file2 = ''
		self.file1_dye = ''
		self.file2_dye = ''
		self.out_file_prefix=None # set prefix to None by default
		self.outputfile = ''
		self.outputfilename = ''
		self.tempoutputfilename = ''
		self.tempoutputfile = ''

		# length of files
		self.file1_len = ''
		self.file2_len = ''
		self.output_len = ''

		# dictionary to translate between sub array numbers and file names
		self.subarray_dict={1:'1_1.txt',2:'1_2.txt',3:'1_3.txt',4:'1_4.txt',5:'2_1.txt',6:'2_2.txt',7:'2_3.txt',8:'2_4.txt'}

    
    def read_input_txt_file(self, inputfile, outputfolder):
        '''this module reads a input txt file (tab delimited with barcode 1, subarray, dye 1, barcode 2, subarray, dye2)
        The subarrays and barcode are converted into a pattern to search for the FEFile and these are put into a list'''

        # set output folder from sys argv and append \\
        self.outputfolder = outputfolder + "\\"

        with open(inputfile, 'r') as file2open:
			# for each line split into columns
			for line in file2open:
				#split line on tab
				splitline=line.split('\t')
				
				
			  # check if any empty lines, or fields are present in input file. do not check prefix (last element in list)
				if '' in splitline[0:7]:
					raise ValueError("\nError in the input file! \nHave you used Excel?!?!?! \n\
					Please open in notepad and ensure there are no blank lines and all fields are present")
					
				# assign each value to a variable
				# barcode, subarray (numeric), dye and scan number for file 1
				file1_barcode=splitline[0]
				file1_subarray=int(splitline[1])
				file1_dye=splitline[2]
				file1_scan_number=splitline[3]
				
				# barcode, subarray (numeric), dye and scan number for file 2
				file2_barcode=splitline[4]
				file2_subarray=int(splitline[5])
				file2_dye=splitline[6]
				file2_scan_number=splitline[7].rstrip()
				
									
				# a prefix can be added to as the last column, which is added to the start of the output filename (len(splitline) == 9)
				if len(splitline)==9:	
					# capture prefix and remove newline
					out_file_prefix=splitline[8].rstrip()
					#check the prefix is not empty
					assert len(out_file_prefix)!= 0,"Prefix column is empty, were you trying to add a prefix??!"
					
					#and append an underscore to help later.
					out_file_prefix=out_file_prefix+"_"
				# if no prefix specified
				else:
					out_file_prefix=None
				
				# check the given subarray values are valid. if they are not the text value will not be returned from the dictionary
				assert file1_subarray in self.subarray_dict, "the given subarray for the Cy3 sample is invalid ("+str(file2_subarray)+")(must be a number 1-8)"
				assert file2_subarray in self.subarray_dict, "the given subarray for the Cy5 sample is invalid ("+str(file2_subarray)+")(must be a number 1-8)"
				
				# convert the given subarray (an integer 1-8 - the keys in self.subarray_dict) into the string used in the file name (the values in self.subarray_dict)
				file1_subarray=self.subarray_dict[file1_subarray]
				file2_subarray=self.subarray_dict[file2_subarray]
								

				# concatenate barcode, scan number and subarray text string to create a filename pattern to search for
				filename1 = str(file1_barcode) + "_S0"+file1_scan_number+"*" + file1_subarray
				filename2 = str(file2_barcode) + "_S0"+file2_scan_number+"*" +file2_subarray

				# append to a list
				self.files_to_find.append((filename1, file1_dye, filename2, file2_dye,out_file_prefix))

    def find_FEfiles(self):
        '''this reads the list created above containing filename pattern and replaces this with the full file name'''
        # for each row of the text file split into fields
        for i in self.files_to_find:
            file1_pattern = i[0]
            file1_dye = i[1]
            file2_pattern = i[2]
            file2_dye = i[3]
            out_file_prefix=i[4]

            # set filename as none to help identify when no match has been found below
            file1_filename = None
            file2_filename = None

            # search for a FE file which matches the filename pattern
            for afile in os.listdir(self.chosenfolder):
                # file 1
                if fnmatch.fnmatch(afile, file1_pattern):
                    file1_filename = afile

                # file 2
                if fnmatch.fnmatch(afile, file2_pattern):
                    file2_filename = afile


            # if both files have been identified add this to a new list else report.
            if file1_filename is not None and file2_filename is not None:
                self.list_of_files.append((file1_filename, file1_dye, file2_filename, file2_dye,out_file_prefix))
            else:
                raise ValueError("no match for " + file1_pattern + " and " + file2_pattern)

    def get_sys_argvs(self, file1_in, dye1_in, file2_in, dye2_in,out_file_prefix):
        '''capture file names and dyes from list as global variables'''
        self.file1 = file1_in
        self.file2 = file2_in
        self.file1_dye = dye1_in
        self.file2_dye = dye2_in
        self.out_file_prefix = out_file_prefix

    def create_dicts(self):
        '''open files, create the temporary file and add features to dictionaries '''
        # open files
        file1_open = open(self.chosenfolder + self.file1, 'r')
        file2_open = open(self.chosenfolder + self.file2, 'r')

        # remove string from filename
        pre_output1 = self.file1.replace("_Guys121919_CGH_1100_Jul11", '')
        pre_output2 = self.file2.replace("_Guys121919_CGH_1100_Jul11", '')
        
        # check if prefix is present
        if out_file_prefix is not None:
            # concatenate prefix, filenames and dyes into output filename file1_file1_dye_file2_file2_dye.txt
            self.outputfilename = self.out_file_prefix+pre_output1.replace(".txt", '') + "_" + self.file1_dye + "_" + pre_output2.replace(".txt", '') + "_" + self.file2_dye + ".txt"
        #if no prefix:
        else:
            # concatenate filenames and dyes into output filename file1_file1_dye_file2_file2_dye.txt
            self.outputfilename = pre_output1.replace(".txt", '') + "_" + self.file1_dye + "_" + pre_output2.replace(".txt", '') + "_" + self.file2_dye + ".txt"

        # add temp to end of file name to create a temporary output filename
        self.tempoutputfilename = self.outputfilename.replace(".txt", '') + "temp.txt"

        # open temp output file
        self.tempoutputfile = open(self.outputfolder + self.tempoutputfilename, 'w')

        # open file1 and create a dict of the features.
        for i, line in enumerate(file1_open):
            if i >= 10:
                splitline = line.split('\t')
                self.file1_dict[int(splitline[1])] = line
                # get n of rows in file1
                self.file1_len = i

        # repeat for features in second file but first writing the feparam and stats to temp file - when pairing with control this ensures the "header" comes from the test (file2) not control (file1), NB NEITHER ARE ACCURATE!!!!
        
        for j, line in enumerate(file2_open):
            if j < 10:
                self.tempoutputfile.write(line)
            # then add all features to a dictionary, with the unique feature number as a key
            if j >= 10:
                splitline = line.split('\t')
                self.file2_dict[int(splitline[1])] = line
                # get n of rows in file2
                self.file2_len = j

        # close files
        file1_open.close()
        file2_open.close()

    def rewrite_file(self):
        '''extract the desired sample(dye) from the dictionaries and re-write the fefile'''

        # get the specified dye for each file
        if str(self.file1_dye) in ("cy3", "Cy3", "CY3") and str(self.file2_dye) in ("cy3", "Cy3", "CY3"):

            # Sort the dictionary on the keys so the file is in order of feature number. remove newline
            for i in sorted(self.file1_dict.keys()):
                file1_line = self.file1_dict[i].rstrip()
                # for each feature split the line on tab and assign to f1
                f1 = file1_line.split('\t')
                # pull out the corresponding feature from file 2, split and assign to f2
                file2_line = self.file2_dict[i].rstrip()
                f2 = file2_line.split('\t')

                # Variables used to concatenate the line to write to file
                t = "\t"  # join
                logratio = math.log(float(f2[13]) / float(f1[13]), 10)  # calculate the log ratio
                logratioerr = str(0)
                pval = str(0)

                # concatenate all the columns as required depending on the dyes selected. NB use of same f1 and f2 columns as the dyes are the same!
                to_write = f1[0] + t + f1[1] + t + f1[2] + t + f1[3] + t + f1[4] + t + f1[5] + t + f1[6] + t + f1[7] + t + f1[8] + t + f1[9] + t + str(logratio) + t + logratioerr + t + pval + t + f1[13] + t + f2[13] + t + f1[15] + t + f2[15] + t + f1[17] + t + f2[17] + t + f1[19] + t + f2[19] + t + f1[21] + t + f2[21] + t + f1[23] + t + f2[23] + t + f1[25] + t + f2[25] + t + f1[27] + t + f2[27] + t + f1[29] + t + f2[29] + t + f1[31] + t + f2[31] + t + f1[33] + t + f1[34] + t + f2[34] + t + f1[36] + t + f2[36] + t + f1[38] + t + f2[38] + t + f1[40] + t + f1[41] + t + f2[41] + "\n"

                # write this to the temporary output file
                self.tempoutputfile.write(to_write)

        # repeat for all combinations of dye

        if str(self.file1_dye) in ("cy3", "Cy3", "CY3") and str(self.file2_dye) in ("cy5", "Cy5", "CY5"):
            for i in sorted(self.file1_dict.keys()):
                file1_line = self.file1_dict[i].rstrip()
                f1 = file1_line.split('\t')

                file2_line = self.file2_dict[i].rstrip()
                f2 = file2_line.split('\t')
                t = "\t"
                logratio = math.log(float(f2[14]) / float(f1[13]), 10)
                logratioerr = str(0)
                pval = str(0)
                # note different columns from f1+f2 selected as different dyes
                to_write = f1[0] + t + f1[1] + t + f1[2] + t + f1[3] + t + f1[4] + t + f1[5] + t + f1[6] + t + f1[7] + t + f1[8] + t + f1[9] + t + str(logratio) + t + logratioerr + t + pval + t + f1[13] + t + f2[14] + t + f1[15] + t + f2[16] + t + f1[17] + t + f2[18] + t + f1[19] + t + f2[20] + t + f1[21] + t + f2[22] + t + f1[23] + t + f2[24] + t + f1[25] + t + f2[26] + t + f1[27] + t + f2[28] + t + f1[29] + t + f2[30] + t + f1[31] + t + f2[32] + t + f1[33] + t + f1[34] + t + f2[35] + t + f1[36] + t + f2[37] + t + f1[38] + t + f2[39] + t + f1[40] + t + f1[41] + t + f2[42] + "\n"
                self.tempoutputfile.write(to_write)

        if str(self.file1_dye) in ("cy5", "Cy5", "CY5") and str(self.file2_dye) in ("cy3", "Cy3", "CY3"):
            for i in sorted(self.file1_dict.keys()):
                file1_line = self.file1_dict[i].rstrip()
                f1 = file1_line.split('\t')

                file2_line = self.file2_dict[i].rstrip()
                f2 = file2_line.split('\t')
                t = "\t"
                logratio = math.log(float(f2[13]) / float(f1[14]), 10)
                logratioerr = str(0)
                pval = str(0)
                to_write = f1[0] + t + f1[1] + t + f1[2] + t + f1[3] + t + f1[4] + t + f1[5] + t + f1[6] + t + f1[7] + t + f1[8] + t + f1[9] + t + str(logratio) + t + logratioerr + t + pval + t + f1[14] + t + f2[13] + t + f1[16] + t + f2[15] + t + f1[18] + t + f2[17] + t + f1[20] + t + f2[19] + t + f1[22] + t + f2[21] + t + f1[24] + t + f2[23] + t + f1[26] + t + f2[25] + t + f1[28] + t + f2[27] + t + f1[30] + t + f2[29] + t + f1[32] + t + f2[31] + t + f1[33] + t + f1[35] + t + f2[34] + t + f1[37] + t + f2[36] + t + f1[39] + t + f2[38] + t + f1[40] + t + f1[42] + t + f2[41] + "\n"
                self.tempoutputfile.write(to_write)

        if self.file1_dye in ("cy5", "Cy5", "CY5") and self.file2_dye in ("cy5", "Cy5", "CY5"):
            for i in sorted(self.file1_dict.keys()):
                file1_line = self.file1_dict[i].rstrip()
                f1 = file1_line.split('\t')

                file2_line = self.file2_dict[i].rstrip()
                f2 = file2_line.split('\t')
                t = "\t"
                logratio = math.log(float(f2[14]) / float(f1[14]), 10)
                logratioerr = str(0)
                pval = str(0)
                to_write = f1[0] + t + f1[1] + t + f1[2] + t + f1[3] + t + f1[4] + t + f1[5] + t + f1[6] + t + f1[7] + t + f1[8] + t + f1[9] + t + str(logratio) + t + logratioerr + t + pval + t + f1[14] + t + f2[14] + t + f1[16] + t + f2[16] + t + f1[18] + t + f2[18] + t + f1[20] + t + f2[20] + t + f1[22] + t + f2[22] + t + f1[24] + t + f2[24] + t + f1[26] + t + f2[26] + t + f1[28] + t + f2[28] + t + f1[30] + t + f2[30] + t + f1[32] + t + f2[32] + t + f1[33] + t + f1[35] + t + f2[35] + t + f1[37] + t + f2[37] + t + f1[39] + t + f2[39] + t + f1[40] + t + f1[42] + t + f2[42] + "\n"
                self.tempoutputfile.write(to_write)

        # close temp file now it's written
        self.tempoutputfile.close()

    def calculate_DLRS(self):
        '''To calculate the DLRS the newly created temp file is read.
        The chromosome, start and log ratio are added to a new array
        This array is sorted on genomic coords.
        Maintaining this order a list of all the log ratios for each chrom are added to a dictionary with chrom as the key.
        For each chromosome the list is read and the previous log ratio is subtracted to create a list of derivatives (differences between probes)
        The interquartile ranges are calculated and only the middle 50% of derivatves are kept.
        The SD of these derivatives is calculated
        This is then put into the stats line and the final output file is created
        '''
        # open tempoutput file as read only
        tempoutputfile = open(self.outputfolder + self.tempoutputfilename, 'r')
        for i, line in enumerate(tempoutputfile):
            # for all features:
            if i >= 10:
                splitline = line.split('\t')
                # remove all control probes and check that there are the correct number of columns
                if int(splitline[5]) == 0 and len(splitline) == 43:
                    # split the genomic location into three new fields
                    genloc = splitline[7]
                    splitgenloc = genloc.replace('chr', '').replace('-', ':').split(':')

                    # change X and Y to numerical
                    splitgenloc[0] = splitgenloc[0].replace('X', '23').replace('Y', '24')

                    # insert the split genomic location into the line
                    splitline.insert(8, int(splitgenloc[0]))
                    splitline.insert(9, int(splitgenloc[1]))
                    splitline.insert(10, int(splitgenloc[2]))

                    # append to an array (chrom, start and gprocessedsignal,rprocessedsignal)
                    self.array1.append((splitline[8], splitline[9], splitline[16], splitline[17]))

                elif int(splitline[5]) == 0 and len(splitline) != 43:
                    raise ValueError("temp file feature length !=43")

            else:
                pass
        tempoutputfile.close()

        # sort the arrays so probes are in genomic order
        self.sortedarray = sorted(self.array1, key=lambda tup: tup[1])
        self.sortedarray = sorted(self.sortedarray, key=lambda tup: tup[0])

        # go through each chromosome in order, and pull out the log ratio scores from the array (these should be in order) and add to a list. Add this list to a dictionary with the key as chromosome number
        for i in range(1, 25):
            alist = []
            for k in self.sortedarray:
                if k[0] == i:
                    # taking processed signal int calculate the log2 ratio: log2(red/green)
                    log2 = math.log(numpy.divide(float(k[3]), float(k[2])), 2)
                    alist.append(log2)
            self.log_dict[i] = alist
            # self.log_dict is {(chrom: 'probe1 log score','probe 2 log score'...).(chrom2:'probe1 log score;,...)}

        # for each chromosome (i is the key (chrom))
        for i in self.log_dict:
            # how many probes are there
            num_of_probes = len(self.log_dict[i])
            # for that number of probes
            for j in range(num_of_probes):
                # excluding the first probe (as there is no probe to subtract)
                if j > 0:
                    # pull out log ratio and calculate the difference between that and the previous probe. subtract the previous one from this probe and append to a new list
                    n = float(self.log_dict[i][j]) - float(self.log_dict[i][j - 1])
                    self.all_derivatives.append(n)

        ########################################################################
        #  create a file containing only the derivatives to help in DLRS calculations
        #  open file with prefix DLRS_
        #  DLRSFile=open(self.outputfolder+"DLRS_"+self.outputfilename,'w')
        #
        #  sort list of derivatives
        #  self.all_derivatives=sorted(self.all_derivatives)
        #  write derivative to file
        #  for i in self.all_derivatives:
        #      DLRSFile.write(str(i)+"\n")
        #  DLRSFile.close()
        ########################################################################

        # calculate DLRS
        # get 1st and 3rd quartile
        q75, q25 = numpy.percentile(self.all_derivatives, [75, 25])
        # calculate 1st quartile-3rd quartile and divide by 1.35
        DLRS = numpy.divide(q75 - q25, 1.35)
        sqrt2 = numpy.sqrt(2)
        DLRS_sqrt = numpy.divide(DLRS, sqrt2)

        ########################################################################
        #  old DLRS
        #  use numpy to get the 25 and 75 percentile
        #  q75,q25=numpy.percentile(self.all_derivatives,[75,25])
        #  for i in self.all_derivatives:
        #      if q25< i <q75:
        #          self.filtered_derivatives.append(i)
        #  print "len of all_derivatives: "+str(len(self.all_derivatives))
        #  print "len of filtered SD: "+str(len(self.filtered_derivatives))
        ########################################################################
        
        ########################################################################
        #
        #  calculate the DLSR by calculating the SD of this list
        #  DLSR=numpy.std(self.filtered_derivatives)
        #  sqrt2=numpy.sqrt(2)
        #  DLSR_sqrt=numpy.divide(DLSR,sqrt2)
        ########################################################################

        # open the final output file
        if os.path.isfile(self.outputfolder + self.outputfilename):
            self.report.append(str(self.outputfilename) + " was not created as it already existed\n")
        else:
            self.report.append(str(self.outputfilename) + " created succesfully\n")
            
            
            finaloutput = open(self.outputfolder + self.outputfilename, 'w')
            tempoutputfile = open(self.outputfolder + self.tempoutputfilename, 'r')
    
            # loop through the temp file and print it to a new file
            for i, line in enumerate(tempoutputfile):
                if i != 6:
                    finaloutput.write(line)
                # except for line 7 which needs the DLSR updating
                elif i == 6:
                    splitline = line.split('\t')
                    splitline[118] = str(DLRS_sqrt)
                    to_add = '\t'.join(splitline)
                    finaloutput.write(to_add)
    
            # get n of rows in output file
            self.output_len = i
    
            ########################################################################
            #  print "self.file1_len "+str(self.file1_len)
            #  print "self.file2_len "+str(self.file2_len)
            #  print "self.output_len "+str(self.output_len)
            ########################################################################
    
            # check the output file is the same length as the two input files.
            assert self.file1_len == self.file2_len, "Two input files are not the same length"
            assert self.file1_len == self.output_len, "Output file is not the same length as input files"
    
            # close files
            tempoutputfile.close()
            finaloutput.close()

        # delete temporary file
        os.remove(self.outputfolder + self.tempoutputfilename)

        # clear all varaiables
        self.file1_dict.clear()
        self.file2_dict.clear()
        del self.filtered_derivatives[:]
        del self.array1[:]
        del self.sortedarray[:]
        self.log_dict.clear()
        del self.all_derivatives[:]
        del self.filtered_derivatives[:]


if __name__ == '__main__':
    # counter
    n = 1
    
    #print "starting EvE"
    
    # input text file
    # input_textfile="S:\\Genetics_Data2\\Array\\Audits and Projects\\150702 PGD FEfiles\\round 2\\eve_input.txt"
    input_textfile = (sys.argv[1])

    # second argument is output folder
    outputfolder = (sys.argv[2])

    # instance of the class
    a = Merge_FEfile()
    # send to function the input text file and outputfolder
    a.read_input_txt_file(input_textfile, outputfolder)
    # Call module to find the matching FE file
    a.find_FEfiles()

    # loop through the list of files creating desired output.
    for i in a.list_of_files:
        if len(i) == 5:
            # create variables of file1, dye, file2, dye, prefix
            file_in_1 = i[0]
            file_in_2 = i[2]
            file_in_1_dye = i[1]
            file_in_2_dye = i[3]
            out_file_prefix=i[4]

            # create if statement to allow unit test to bypass assert statement
            if file_in_1 in ("File1_S01_1_1.txt", "File2_S01_1_1.txt") and file_in_2 in ("File1_S01_1_1.txt", "File2_S01_1_1.txt"):
                pass
            else:
                # assert the array design is the same (get the array design from barcode)
                file_in_1_design = file_in_1[2:7]
                file_in_2_design = file_in_2[2:7]
                assert file_in_1_design == file_in_2_design, "The two arrays are not the same design."

            # send variables to get_sys_argvs
            a.get_sys_argvs(file_in_1, file_in_1_dye, file_in_2, file_in_2_dye,out_file_prefix)
            # open these files and put into dictionarys
            a.create_dicts()
            # pull out desired rows and write to temp file
            a.rewrite_file()
            # calculate DLRS and write to final output file
            a.calculate_DLRS()
        else:
            print "error in input file for " + i
    for i in a.report:
        print i
    print "files created in: " + outputfolder
    #print "done file " + str(n) + " of " + str(len(a.list_of_files))
    n = n + 1
