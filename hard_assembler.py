#hard assembler#
import copy
from extract_haplotype import *
from easy_assembler import *

def if_overlap_multi(h_hash, read):
    overlap = []
    for each_hash in h_hash:
        overlap.append(if_overlap(each_hash, read))
    return overlap


def calculate_freq (hx_hash, read, overlap_index, last_index):
    freq = 0
    for i in range(overlap_index, last_index):
        if read[i] == '1':
            freq = freq+ float(hx_hash[i]['1'])/float(hx_hash[i]['total'])
        elif read[i] == '0':
            freq = freq+ float(hx_hash[i]['0'])/float(hx_hash[i]['total'])
    return freq


def multi_plug_h(h_hash, read, overlap_index):
    freq = []
    unused = []
    for i in range(0, len(h_hash)):
        if overlap_index[i] >=0:
            last_index= hash_last_valid(h_hash[i])
            this_freq = calculate_freq(h_hash[i], read, overlap_index[i],last_index)
            freq.append(this_freq)
        else:
            count_not_0 = 0
            #print h_hash[i]
            for each in h_hash[i]:
                if h_hash[i][each]['total'] > 0:
                    count_not_0 = 1
                    break
            if count_not_0 ==0:
                unused.append(i)
            freq.append(0)
    max_freq = 0
    max_index = -1
    for i in range(0,len(freq)):
        if freq[i] > max_freq:
            max_freq = freq[i]
            max_index = i
    if max_freq < 0.80:
        #print "max_freq<0.5"
        if len(unused)>0:
            forward_plug_h0(h_hash[unused[0]],read)
            #print unused
            return 1
        else:
            if max_freq >0.75:
                forward_plug_h0(h_hash[max_index], read)
            #print "returnning -1"
            else:
                return -1 #meaning save to temp_container
    else:
        forward_plug_h0(h_hash[max_index], read)
        return 1



def read_first_valid(read):
    for i in range(0, len(read)):
        if read[i] != '-':
            return i

def hash_first_valid(h_hash):
    valid_bit = -1
    for each in h_hash:
        if int(each.keys()[0])>valid_bit:
            valid_bit = int(each.keys()[0])
    return valid_bit


def try_plug_error(h_hash, temp_container):
    success_error = []
    for i in range(0, len(temp_container)):
        error_read = temp_container[i]
        read_first_bit = read_first_valid(error_read)
        hash_first_bit = hash_first_valid(h_hash)
        if read_first_bit > hash_first_bit:
            overlap = if_overlap_multi(h_hash, error_read)
            #print "try plug error"
            plug_result = multi_plug_h(h_hash, error_read, overlap)
            if plug_result == 1:
                success_error.append(i)
    
       
def multi_extract_haplotype(file_name):
    file_path = "/Users/qinyiyan/Dropbox/ucla/2016spring/224/proj/Final_2/" + file_name
    l = []
    with open(file_path, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            #print len(line)
            if len(line) > 0:
                l.append(map(str, line.split(',')))
    return l

def hard_assembler(reads, n):
    num_read = len(reads[0])
    print "num_read = "+str(num_read)
    h = []*n
    h_hash = []
    for i in range(0,n):
        hh_hash = {}
        h_hash.append(hh_hash)
    temp_container = []
    error_count = 0
    possible_hash = []
    for i in range(0, num_read):
        for j in range(0,n):
            h_hash[j][i] = {}
            h_hash[j][i]['0'] = 0
            h_hash[j][i]['1'] = 0
            h_hash[j][i]['total'] = 0
    #print "read[0]="+reads[0]
    forward_plug_h0 (h_hash[0], reads[0])
    
    for i in range(1, len(reads)):#for each read:
        #print "reads index: "+str(i)
        overlap = if_overlap_multi(h_hash, reads[i])
        #print overlap
        #print h_hash[3][99]
        non_overlap = []
        overlapped = []
        
        for j in range(0, len(overlap)):
            if overlap[j] <0:
                non_overlap.append(j)
            else:
                overlapped.append(j)
        non_overlap_length = len(non_overlap)
        #print "non_overlap"
        #print non_overlap
        #print "overlap"
        #print overlap
        if non_overlap_length == 4:
            print non_overlap_length
        if non_overlap_length == 0: #no non_overlap
            plug_result = multi_plug_h(h_hash, reads[i], overlap)
            if plug_result == -1:
#                 print "nonoverlap is "
#                 print non_overlap
#                 print "all overlap plug_result = -1"
                temp_container.append(reads[i])
        elif non_overlap_length ==1: 
            plug_result = multi_plug_h(h_hash, reads[i], overlap)
            if plug_result == -1:
                try_plug_error(h_hash, temp_container)
                overlap = if_overlap_multi(h_hash, reads[i])
                plug_result = multi_plug_h(h_hash, reads[i], overlap)
                if plug_result == -1:
#                     print "one not overlap"
#                     print "nonoverlapis "
#                     print non_overlap
                    forward_plug_h0(h_hash[non_overlap[0]],reads[i])
        else: #>2 overlap
            plug_result = multi_plug_h(h_hash, reads[i], overlap)
            #print "plug result = "+str(plug_result)
            if plug_result == -1:
                try_plug_error(h_hash, temp_container)
                overlap = if_overlap_multi(h_hash, reads[i])
            plug_result = multi_plug_h(h_hash, reads[i], overlap)
            if plug_result == -1:
#                 print non_overlap
#                 print ">2 no overlap plug result = -1"
            #point to a box
                new_index = read_first_valid(reads[i])
                #print "new_index="+str(new_index)
                new_hash_list = []
                new_hash = {}
                for index in range(new_index, num_read):
                    new_hash[index] = {}
                    new_hash[index]['0'] = 0
                    new_hash[index]['1'] = 0
                    new_hash[index]['total'] = 0
                forward_plug_h0(new_hash,reads[i])
                new_hash_list.append(new_hash)
                for count in range(1, non_overlap_length):
                    new_hash_2 = {}
                    for index in range(new_index, num_read):
                        new_hash_2[index] = {}
                        new_hash_2[index]['0'] = 0
                        new_hash_2[index]['1'] = 0
                        new_hash_2[index]['total'] = 0
                    new_hash_list.append(new_hash_2)
                    
                count_new_hash = 0
                for nonoverlap_hash_index in non_overlap:
                    for index in range(new_index+1, num_read):
                        del h_hash[nonoverlap_hash_index][index]
                    h_hash[nonoverlap_hash_index][new_index]['total'] = new_hash_list
                    possible_hash.append(h_hash[nonoverlap_hash_index])
                    h_hash[nonoverlap_hash_index] = new_hash_list[count_new_hash]
                    count_new_hash += 1
    
    if len(temp_container)>0:
        try_plug_error(h_hash, temp_container)
            
    
    for each in h_hash:
        possible_hash.append(each)
    return possible_hash    
          
 
 
def hashlist_to_possibilities(haplotypes, hash_list):
    indexes = hash_list[0].keys()
    new_hash_list = []
    #print hash_list
    #print indexes[0:-1]
    #haplotypes = []*4
    #print hash_list[0][indexes[-1]]['total']
    for each in hash_list:
        if len(each) < len(indexes):
            indexes = each.keys()
    #print indexes
#     print "index[-1]is " + str(indexes[-1])
#     if indexes[-1] == 998:
#         print indexes[0]
    index = indexes[0]
    for i in indexes[0:-1]:#0 to the index of the next_hash
        for j in range(0, len(hash_list)):
            if hash_list[j][i]['0']>hash_list[j][i]['1']:
                haplotypes[j].append('0')
            elif hash_list[j][i]['0']<hash_list[j][i]['1']:
                haplotypes[j].append('1')
            else:
                if hash_list[j][i]['total'] == 0:
                    haplotypes[j].append('x')
                else:
                    haplotypes[j].append('?')
        index = index+1
    point_to_next_hash_string = []
    not_next_hash_string = []
    count_next = 0
    
    for j in range(0, len(hash_list)):
        if type(hash_list[j][indexes[-1]]['total']) is list:
            #print "true"
            point_to_next_hash_string.append(j)
#             print "j is"+str(j)
#             if indexes[-1] == 998:
#                 print hash_list[j]
#             print "compare"
#             print len(hash_list[j][indexes[-1]]['total'])
#             print count_next
#             print indexes[-1]
            new_hash_list.append(hash_list[j][indexes[-1]]['total'][count_next])
            count_next = count_next +1
        else:
            hash_sub = {}
            not_next_hash_string.append(j)
            #print hash_list[j].keys()[-1]
            for new_hash_index in range(indexes[-1], hash_list[j].keys()[-1]):
                hash_sub[new_hash_index] = {}
                #hash_sub[new_hash_index] = copy.deepcopy(hash_list[j][new_hash_index])
                hash_sub[new_hash_index]['0'] = hash_list[j][new_hash_index]['0']
                hash_sub[new_hash_index]['1'] = hash_list[j][new_hash_index]['1']
                hash_sub[new_hash_index]['total'] = (hash_list[j][new_hash_index]['total'])
            hash_sub[hash_list[j].keys()[-1]] = copy.deepcopy(hash_list[j][hash_list[j].keys()[-1]])
            #print hash_sub
            new_hash_list.append(hash_sub)
    #print point_to_next_hash_string
    #print count_next
    #print not_next_hash_string
    return (haplotypes, new_hash_list, index, point_to_next_hash_string, not_next_hash_string, count_next)


def deep_copy(haplotypes):
    new_haplotypes = []
    for each in haplotypes:
        new_h = []
        for bit in each:
            new_h.append(bit)
        new_haplotypes.append(new_h)
    return new_haplotypes


def shuffle(hash_list,hash_shuffle_inst, not_shuffle_index):
#     print hash_shuffle_inst
#     print not_shuffle_index
    shuffle_hash = {}
    new_hash_list = []
    for i in range(0, len(hash_list)):
        if i in not_shuffle_index:
            shuffle_hash[i] = hash_list[i]
    for i in hash_shuffle_inst:
        for j in range(0, len(hash_list)):
            if j not in shuffle_hash.keys():
                shuffle_hash[j] = hash_list[i]
                break
    for i in shuffle_hash:
        new_hash_list.append(shuffle_hash[i])
    #print new_hash_list
    return new_hash_list
    

import math
import itertools  

def make_possibilities(haplotypes, hash_list, count_num, point_to_next_hash_string,not_next_hash_string, haplotype_list_container):
    possibility_count = math.factorial(count_num)
    hash_shuffle_list = list(itertools.permutations(point_to_next_hash_string,count_num))
    
    for i in range(0,possibility_count ):
        new_haplotype = deep_copy(haplotypes)
        #print hash_list[3]
        new_hash_list = shuffle(hash_list,hash_shuffle_list[i], not_next_hash_string)  
        #print new_hash_list
        (sub_haplotypes, sub_new_hash_list, sub_index, sub_point_to_next_hash_string, sub_not_shuffle_index, sub_count_next)= hashlist_to_possibilities(new_haplotype, new_hash_list)
        if sub_count_next != 0:
            #print "call make possi"
            make_possibilities(sub_haplotypes, sub_new_hash_list, sub_count_next, sub_point_to_next_hash_string, sub_not_shuffle_index, haplotype_list_container)
        else:
            #print "put to container"
            haplotype_list_container.append(sub_haplotypes)
            
    return haplotype_list_container



def array_to_string_multi(possibilities):
    all_possibilities = []
    for each in possibilities:
        all_possibilities.append(array_to_string(each))
    return all_possibilities



     