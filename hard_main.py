#hard_main#
import sys
import re
from hard_assembler import *
from process_result import *
from extract_haplotype import *

filename = sys.argv[1]
read_data =  multi_extract_haplotype(filename)
multi_data = array_to_string(read_data)

m = re.match('.*(\d)_chromosome',filename)
num_chromosome = int(m.group(1))
print num_chromosome

print len(multi_data)


multi_h_hash_list = hard_assembler(multi_data,num_chromosome)
#print multi_h_hash_list[1]
print len(multi_h_hash_list)


multi_haplotypes = []
initial_hash_list = []
#print multi_h_hash_list[0][98]


for each in multi_h_hash_list:
    if each.keys()[0] == 0:
        initial_hash_list.append(each)
        multi_haplotypes.append([])
#print len(initial_hash_list)
#print multi_haplotypes
(haplotypes, new_hash_list, index, point_to_next_hash_string, not_next_hash_string, count_next)= hashlist_to_possibilities(multi_haplotypes, initial_hash_list)

haplotype_list_container = []
possibilities= make_possibilities(haplotypes, new_hash_list, count_next, point_to_next_hash_string,not_next_hash_string, haplotype_list_container)

all_possibilities = array_to_string_multi(possibilities)
print "possibilities: "+str(len(all_possibilities))
#print len(all_possibilities[0][0])

output_file = "/Users/qinyiyan/Dropbox/ucla/2016spring/224/proj/Final_2/output/hard_output.txt"
f=open(output_file,'w')
for n in range(0, len(all_possibilities)):
	for i in range(0, num_chromosome):
		f.write(all_possibilities[n][i])
		f.write('\n')
	f.write('\n\n')