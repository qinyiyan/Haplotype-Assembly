# easy main
import sys
from easy_assembler import *
from process_result import *
from extract_haplotype import *

filename = sys.argv[1]

(read_data, homo_col) =  extract_haplotype(filename)
easy_data = array_to_string(read_data)
# print homo_col
# print easy_data

easy_h0_list = easy_assemble(easy_data)

easy_h1_list = []
#print easy_h0_list
for each in easy_h0_list:
    oppo_each = []
    for bit in each:
        if bit == "1":
        	#print "yest"
        	oppo_each.append("0")
        else:
        	oppo_each.append("1")
    easy_h1_list.append(oppo_each)

#print easy_h1_list


h0_h1 = [easy_h0_list,easy_h1_list ]
possibilities = get_possibilities2(h0_h1)
#print possibilities
possibilities_h1 = []
for each in possibilities:
	oppo_each = []
	for bit in each:
		if bit == "1":

			oppo_each.append("0")
		else:
			
			oppo_each.append("1")
	
	possibilities_h1.append(oppo_each)
#print possibilities_h1
# gen_list =  haplotype_to_genotype (easy_h0_list, homo_col)
# gen_opposite_list = haplotype_to_genotype (easy_h1_list, homo_col)
#check the length
# h0_length = 0
# for h0 in range (0,len(gen_list)):
#         #print h0_list[h0]
#     h0_length = len(gen_list[h0])+h0_length
# if h0_length != len(read_data[0])+len(homo_col):
# 	print "length not match"
string_h0 = []
for each in possibilities:

	each = haplotype_to_genotype (each, homo_col)
	#each = array_to_string(each)

	string_h0.append(''.join(each))

string_h1 = []
for each in possibilities_h1:
	each = haplotype_to_genotype (each, homo_col)
	string_h1.append(''.join(each))
	

# gen_list_string =  array_to_string(gen_list)
# gen_oppo_string = array_to_string(gen_opposite_list)



######make possibilities######
# count = 0
# genotype_possibilities = []
# (genotype0, genotype1) = ([],[])
# h0orh1_vector = [0,1]
    
# easy_possibilities = add_a_chunk(h0_h1, genotype0, genotype1, count, h0orh1_vector, genotype_possibilities)
# possibilities_string = []
# for each in easy_possibilities:
#     possibilities_string.append(array_to_string(each))



# print "possibilities is: "+str(len(possibilities))
# print "length of haplotype is: "+str(len(possibilities[0][0]))

output_file = "/Users/qinyiyan/Dropbox/ucla/2016spring/224/proj/Final_2/output/easy_output.txt"
f=open(output_file,'w')
for n in range(0, len(possibilities)):
	f.write(string_h0[n])
	f.write('\n')
	f.write(string_h1[n])
	f.write('\n\n')

###########test easy ##########
if len(sys.argv)>2:
	answer_file_name= sys.argv[2]
	answer_file_path = "/Users/qinyiyan/Dropbox/ucla/2016spring/224/proj/Final_2/" + answer_file_name
	answer_file = open(answer_file_path,'r')
	answer_h0h1 = answer_file.readlines()

	easy_answer = parse_answer(answer_file_name)
	answer_haplotype = easy_answer[0]
	
	answer_homo_col = easy_answer[1][0:-1]
	answer_genotype = easy_answer[2][0].strip()

	print "match homo col precision: "
	print match_homo_index (homo_col.keys(), answer_homo_col)
	


	(error_rate, genotype) = match_genotype2(gen_list, gen_opposite_list, answer_genotype)
	#(homo_err,haplotype_err) = error_analysis(error_index, answer_homo_col)
	
	print "error rate is: "+str(error_rate)

	
