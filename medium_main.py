#medium main#

import sys
import copy
from medium_assembler import *
from process_result import *
from extract_haplotype import *


filename = sys.argv[1]
(read_data, homo_col) =  extract_haplotype(filename)
print "homo: "+str(len(homo_col))

medium_data = array_to_string(read_data)

medium_h0_list = medium_assemble(medium_data)
#print medium_h0_list

medium_h1_list = []
for each in medium_h0_list:
    oppo_each = []
    for bit in each:
        if bit == "1":
            oppo_each.append("0")
        else:
            oppo_each.append("1")
    medium_h1_list.append(oppo_each)


h0_h1 = [medium_h0_list, medium_h1_list]
possibilities = get_possibilities2(h0_h1)
#print medium_h0_list[0]
# print len(possibilities[0])
# print "what"
# #print possibilities[0][0]
# print "possibilities: "+ str(len(possibilities))
possibilities_h1 = []
for each in possibilities:
    oppo_each = []
    for trunk in each:
        oppo_trunk = []
        for bit in trunk:
            if bit == "1":
                oppo_trunk.append("0")
            else:
                oppo_trunk.append("1")
        oppo_each.append(oppo_trunk)
    possibilities_h1.append(oppo_each)
#print possibilities_h1
    
string_h0 = []
#print homo_col

for each in possibilities:
    #print each
#     print len(each)
    each_new = haplotype_to_genotype (each, homo_col)
    #print "each_new length" +str(len(each_new))
	#each = array_to_string(each)

    string_h0.append(''.join(each_new))
# print "string_h0 length"+str(len(string_h0[0]))
# print string_h0
string_h1 = []

for each in possibilities_h1:
    each_new = haplotype_to_genotype (each, homo_col)
#     print each
#     print homo_col
    string_h1.append(''.join(each_new))

#print len(string_h1)
# print string_h0[0][837]

#print len(string_h1[0])
output_file = "/Users/qinyiyan/Dropbox/ucla/2016spring/224/proj/Final_2/output/medium_output.txt"
f=open(output_file,'w')
for n in range(0, len(possibilities)):
    f.write(string_h0[n])
    f.write('\n')
    f.write(string_h1[n])
    f.write('\n\n')


#########test medium #######
if len(sys.argv)>2:
	answer_file = sys.argv[2]
	answer_file_path = "/Users/qinyiyan/Dropbox/ucla/2016spring/224/proj/data/" + answer_file
	medium_answer = parse_answer(answer_file)
	answer_haplotype = medium_answer[0]
	answer_homo_col = medium_answer[1][0:-1]
	answer_genotype = medium_answer[2][0].strip()

	print match_homo_index (homo_col.keys(), medium_answer[1])


	(error_rate, genotype) = match_genotype2(gen_list,gen_opposite_list, answer_genotype)
	#(homo_err,haplotype_err) = error_analysis(error_index, answer_homo_col)
	# print homo_err
	# print haplotype_err
	#error_rate = float(len(homo_err)+len(haplotype_err))/float(len(possibilities_string[0][0]))
	print "error rate is: "+str(error_rate)