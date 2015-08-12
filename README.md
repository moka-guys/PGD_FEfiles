# EvE
A python script which takes two samples raw feature extraction (FE) data and combines these into a new FE file.

To run the script takes two arguments, an input file and an output folder.

The input file is a tab delimited text file in the format 
barcode1	subarray1	dye1	barcode2	subarray2	dye2

Each set of barcode, subarray and dye identifies a hyb partner. The first set will become Cy3 and the second set will be Cy5 in the new FE file.

The FE file is created within the folder specified in the second argument.
  

