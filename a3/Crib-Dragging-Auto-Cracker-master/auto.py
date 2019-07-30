import sys
import enchant
import csv

# The English library to validate words
d = enchant.Dict("en_US")

# The minimum length of the crib word
MIN_CRIB_LEN = 5

# The minimun length of the internal partial matching word
# This should be less or equal to MIN_CRIB_LEN
MIN_INTERNAL_LEN = 5 


# Load the 5,000 common English vocabulary library as crib word candidates
with open('FrequentEnglishWordList.csv', 'rb') as f:
    reader = csv.reader(f)
    crib_list = list(reader)
# Remove the header of the list file
crib_list = crib_list[1:]

# This function is credit to https://github.com/SpiderLabs/cribdrag
# @param: 	ctext	- 	The cipher text to be crib dragged
# @param: 	crib 	- 	The crib word to drag on the cipher text
# @return: 	results - 	A list of result that generated from a or partial match
#						of the crib word on the cipher text. Each result is
#						ensured to be an English word and contain letters only
def sxor(ctext, crib):
    results = []
    single_result = ''
    crib_len = len(crib)
    positions = len(ctext)-crib_len+1
    for index in xrange(positions):
        single_result = ''
        for a,b in zip(ctext[index:index+crib_len],crib):
            single_result += chr(ord(a) ^ ord(b))

        # Check the word partially, to see whether it conatins an English word
        result_length = len(single_result)
        if (result_length >= MIN_INTERNAL_LEN):
	        for i in xrange(0, result_length - MIN_INTERNAL_LEN):
	        	for j in xrange(i + MIN_INTERNAL_LEN, result_length):
	        		result_partial = single_result[i:j]
	        		if (result_partial.isalpha()):
	        			if (d.check(result_partial)):
	        				results.append(result_partial + "(" + str(index) + ")")

	    # Check the whole word, to see whether it is an English word
        if (single_result.isalpha()):
	    	if(d.check(single_result)):
	    		results.append(single_result + "(" + str(index) + ")")
	    
    return results

# This function executes the crib dragging of a single word on the cipher text
# And write/append the result to the target output file
def writeResultGivenCrib(ctext, crib):
	results = sxor(ctext, crib)
	results_len = len(results)
	# Write to the output (Append)
	with open(FILE_NAME, "a") as text_file:
		text_file.write(crib + "(" + str(results_len) + "): [ " + ', '.join(results) + " ]\n")

# Provide the Hexidecimal version of cipher_text here
CIPHER_HEX = "8d26d8674d3eb2b9f34e73f6622382a3d9a0ed73bd9a79623a71cf731c9bfdfed006da9a6597f129d9ab85f9058e3e4104566c5381c36071ca1c79425d6a245588da9c56ae48d0af0b3f8e30f720702c672e4b20969a2b56daccd6c9f5bd360106bb1aa827fcec48e832f18bdb08608248550aaec248b1353433f4fe87cc95e79ceb0d429ad5134ece4a6400aa57065aa824dc6adf70e2442c98a4232e71fde9314ca901f7fa0ff95c5f5334ade858ae5a23d7f58081a44ad74e4987041f7b9c7e9c665be68e3ad0ac053800d65cbc279c343076fa5b480d10ac7ce6486c206afb396e5a7b5d78187b70f223b7e7b14520b9fa2fa127fcbf08fed4c1c326a5ebe51bcc467e6e537ce3e9e4b83dc78b6b4f02c8ee1eb337af82810a8a6c0f9792a794c0470714167f720fbc5e"
# Decode the hexidecimal cipher text
cipher_text = CIPHER_HEX.decode('hex')
# File Name
FILE_NAME = "auto_output.txt"

# Clear the content of the output file before starting to append
open(FILE_NAME, 'w').close()

# Iterate through the crib word list
for ind, crib in enumerate(crib_list):
	# Get the column of the word
	crib_word = crib[1]
	print str(ind) + ": " + crib_word
	# Write the result to the file
	if (len(crib_word) >= MIN_CRIB_LEN):
		writeResultGivenCrib(cipher_text, crib_word)
