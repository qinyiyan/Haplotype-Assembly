#medium assembler##
from extract_haplotype import *
from easy_assembler import *

def current_hash_value(h0_hash, index):
    if h0_hash[index]['0']>h0_hash[index]['1']:
        return 0
    elif h0_hash[index]['0']<h0_hash[index]['1']:
        return 1
    else:
        return -1

def flip_opposite(read, oppo_index):
    read_list = list(read)
    for i in oppo_index:
        if read_list[i] == '0':
            read_list[i] = '1'
        elif read_list[i] == '1':
            read_list[i] = '0' 
        else:
            print "read [i] not valid"
    read = ''.join(read_list)
    return read

def try_plug_h0(read, h0_hash, overlap_index, mode = 'strict'):
    upper_threshold= 0.75
    loose_upper_threshold = 0.6
    lower_threshold = 0.25
    loose_lower_threshold = 0.4
    if mode == 'loose':
        upper_threshold= loose_upper_threshold
        lower_threshold= loose_lower_threshold
    
    same = 0
    opposite = 0
    oppo_index = []
    error_count = 0
    #print hash_last_valid(h0_hash)
    for j in range(overlap_index, hash_last_valid(h0_hash)):
        current_bit = current_hash_value(h0_hash, j)
        not_current_bit = 0
        if current_bit == 1:
            #print "a"
            not_current_bit = 0
        elif current_bit ==0:
            #print "b"
            not_current_bit =1
        #else:
            
            #print "current bit not valid"
#         print read[j]
#         print current_bit
#         print not_current_bit
#         print "----"
        if current_bit != -1:
            if read[j] == str(current_bit):
                #print "c"
                same = same+1
                #print same
            elif read[j] == str(not_current_bit):
                #print "d"
                opposite = opposite +1
                oppo_index.append(j)
                #print "oppo"
                #print opposite
    total = same + opposite
#     print "same and oppo"
#     print same
#     print opposite
#     print "total"
#     print total
    if total== 0:
        return (0, error_count) 
    if float(same)/float(total) >0.75:
        read=flip_opposite(read,oppo_index)
        error_count = error_count +1
        forward_plug_h0(h0_hash, read)
        #read = '-'
        #print h0_hash[0]
        return (1,error_count) #denote forward
    elif float(same)/float(total) <0.25:
        read=flip_opposite(read,oppo_index)
        error_count = error_count +1
        forward_plug_h0(h0_hash, read)
        #read = '-'
        #print h0_hash[0]
        return (-1, error_count) #denote reverse
    else:
        #print h0_hash[0]
        return (0, error_count)  #denote not plug



def medium_assemble(reads):
    num_read = len(reads[0])
    h0_hash_index_list = []
    h0_hash = {}
    temp_container = []
    error_count=0
    for i in range(0, num_read):
        h0_hash[i] = {}
        h0_hash[i]['0'] = 0
        h0_hash[i]['1'] = 0
        h0_hash[i]['total'] = 0
    #print reads[0]
    forward_plug_h0 (h0_hash, reads[0])
    #print h0_hash[0]
    for i in range(1, len(reads)):#for each read:
        overlap = if_overlap(h0_hash, reads[i])
        #if no overlap: create another hash_map to record one probable situation: assume it belongs to h0.
        if overlap == -2:#all'-'
            next
        elif overlap == -1:
            print "i is "+str(i)  
            #print hash_last_valid(h0_hash)
            for error_read in temp_container:
                temp_overlap = if_overlap(h0_hash, error_read)
                if temp_overlap != -1 and temp_overlap != -2:
                    try_result = try_plug_h0(error_read, h0_hash, temp_overlap) 
                    if try_result == -1 or try_result == 1:
                        error_read = '-'
                        error_count = error_count + try_result[1]
                
            overlap = if_overlap(h0_hash, reads[i])
            if overlap == -1:           
                h0_hash_index_list.append(hash_last_valid(h0_hash))
                forward_plug_h0(h0_hash, reads[i])
            else:
                try_again =  try_plug_h0(error_read, h0_hash, temp_overlap) 
                if try_again[0] == 0:
                    temp_container.append(reads[i])
                else:
                    error_count = error_count +try_again[1]
        else: #has overlap, returned the index of the first overlapped bit
            #overlap_index = overlap
            try_plug = try_plug_h0(reads[i], h0_hash, overlap) 
            if try_plug[0] == 0:
                temp_container.append(reads[i])
            else:
                error_count = error_count +try_plug[1]
    
    h0_hash_index_list.append(len(h0_hash))
    #print h0_hash_index_list
    
    if len(temp_container)>0:
        for error_read in temp_container:
            temp_overlap = if_overlap(h0_hash, error_read)
            if temp_overlap != -1 and temp_overlap != -2:
                try_result = try_plug_h0(error_read, h0_hash, temp_overlap, 'loose') 
                if try_result == -1 or try_result == 1:
                    error_read = '-'
                    error_count = error_count + try_result[1]

    h0_list = []
    h0 = []

    for key_i in range(0,h0_hash_index_list[0]):
        if h0_hash[key_i]['0']>h0_hash[key_i]['1']:
            h0.append('0')
        elif h0_hash[key_i]['0']<h0_hash[key_i]['1']:
            h0.append('1')
        else:
            h0.append('?')
    h0_list.append(h0)
    
    if len(h0_hash_index_list)>1:
        for i in range(1,len(h0_hash_index_list)):
            #print h0_hash_index_list[i-1]
            #print h0_hash_index_list[i]
            h0 = []
            for key_i in range(h0_hash_index_list[i-1],h0_hash_index_list[i] ):
                if h0_hash[key_i]['0']>h0_hash[key_i]['1']:
                    h0.append('0')
                elif h0_hash[key_i]['0']<h0_hash[key_i]['1']:
                    h0.append('1')
                else:
                    h0.append('?')
            h0_list.append(h0)
    #print "h0_len" +str(len(h0_list[0]))
    return h0_list

