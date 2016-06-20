# easy assembler
import copy
from extract_haplotype import *

def if_overlap (h0_hash, read):
    count = 0
    for i in range(0, len(read)):
        if read[i]== '-':
            count = count+1
        else: #if read[i]!= '-':
            if h0_hash[i]['total']!= 0:
                return i; 
    if count == len(read):
        return -2
    else:
        #print count
        return -1;

def forward_plug_h0(h0_hash, read):
    for i in range(0, len(read)):
        #print len(read)-1
        if read[i] == '0':
            h0_hash[i]['0'] = h0_hash[i]['0']+1
            h0_hash[i]['total'] = h0_hash[i]['total'] + 1
        elif  read[i] == '1':
            h0_hash[i]['1'] = h0_hash[i]['1']+1
            h0_hash[i]['total'] = h0_hash[i]['total'] + 1
def reverse_plug_h0 (h0_hash, read):
    for i in range(0, len(read)):
        if read[i] == '1':
            h0_hash[i]['0'] = h0_hash[i]['0']+1
            h0_hash[i]['total'] = h0_hash[i]['total'] + 1
        elif  read[i] == '0':
            h0_hash[i]['1'] = h0_hash[i]['1']+1
            h0_hash[i]['total'] = h0_hash[i]['total'] + 1
def evenly_plug_h0 (h0_hash, read):
    for i in range(0, len(read)):
        if read[i] == '0':
            h0_hash[i]['0'] = h0_hash[i]['0']+0.5
            h0_hash[i]['1'] = h0_hash[i]['1']+0.5 
            h0_hash[i]['total'] = h0_hash[i]['total'] + 1
        elif  read[i] == '1':
            h0_hash[i]['0'] = h0_hash[i]['0']+0.5
            h0_hash[i]['1'] = h0_hash[i]['1']+0.5
            h0_hash[i]['total'] = h0_hash[i]['total'] + 1


def hash_last_valid(h0_hash):
    count_key = 0
    for key in h0_hash:
        count_key = key
        if h0_hash[key]['total'] == 0:
            return key
    return count_key



def easy_assemble(reads):
    num_read = len(reads[0])
    h0_hash_index_list = []
    h0_hash = {}
    for i in range(0, num_read):
        h0_hash[i] = {}
        h0_hash[i]['0'] = 0
        h0_hash[i]['1'] = 0
        h0_hash[i]['total'] = 0
    #print reads[0]
    forward_plug_h0 (h0_hash, reads[0])
#     print num_read
#     print len(h0_hash)
    
    for i in range(1, len(reads)):#for each read:
        overlap = if_overlap(h0_hash, reads[i])
        #if no overlap: create another hash_map to record one probable situation: assume it belongs to h0.
        if overlap == -2:#all'-'
            next
        elif overlap == -1:
            print "i is "+str(i)  
            print hash_last_valid(h0_hash)
            h0_hash_index_list.append(hash_last_valid(h0_hash))
            forward_plug_h0(h0_hash, reads[i])
            #evenly_plug_h0(h0_hash, reads[i])
        else: #has overlap
            if h0_hash[overlap]['0']>h0_hash[overlap]['1']:
                if (reads[i][overlap] == '0'):
                    forward_plug_h0(h0_hash, reads[i])
                if (reads[i][overlap] == '1'):
                    reverse_plug_h0(h0_hash, reads[i])
            elif h0_hash[overlap]['0']<h0_hash[overlap]['1']:
                if (reads[i][overlap] == '1'):
                    forward_plug_h0(h0_hash, reads[i])
                if (reads[i][overlap] == '0'):
                    reverse_plug_h0(h0_hash, reads[i])
            else:#h0_hash[overlap]['0']==h0_hash[overlap]['1']
                evenly_plug_h0(h0_hash, reads[i])
#     print h0_hash
#     print len(h0_hash)
#     print len(reads[0])
    h0_hash_index_list.append(len(h0_hash))
    #print h0_hash_index_list
    
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

#     if len(h0_hash_list)>1:
#         for h in range(1,len(h0_hash_list)-1):
#             h0_prob = []
#             for key in h0_hash_list[h]:
#                 if h0_hash_list[h][key]['0']>h0_hash_list[h][key]['1']:
#                     h0_prob.append('0')
#                 elif h0_hash_list[h][key]['0']<h0_hash_list[h][key]['1']:
#                     h0_prob.append('1')
#                 else:
#                     h0_prob.append('?')
#             h0_list.append(h0_prob)
    
    
    #print h0_list
    #print "h0_len" +str(len(h0_list[0]))
    return h0_list
            

def haplotype_to_genotype(h0_list, homo_col):
    homo_col_index = homo_col.keys()
    g0_list = []
    #print len(h0_list)
    h0_length = 0
    for h0 in range (0,len(h0_list)):
        #print h0_list[h0]
        h0_length = len(h0_list[h0])+h0_length
#     print h0_length
#     print len(homo_col)
    
    
    
    count = 0
    #print g0_list
    #print homo_col[0]
    for h in range(0,len(h0_list)):
        ii = 0
        i=0
        while i < len(h0_list[h]):
        #for i in range(0, len(h0_list[h])):
            #print i
            #print count+ii
            if (count + ii) in homo_col:
                #print h
                #print count + ii 
                #print "hhh"
                g0_list.append(str(homo_col[count+ii]))
                ii = ii+1
                
            else:
                g0_list.append(h0_list[h][i])
                ii = ii+1
                i = i+1
        count = count + ii 
    #count = count+1
    while count < h0_length+len(homo_col):
        g0_list.append(str(homo_col[count]))
        count = count +1
    
    the_list = []
    for l in g0_list:
        the_list.append(l[0])
    #print "list length"+str(len(the_list))
    return the_list

def get_possibilities2(h0_h1):
    possibilities = []
    possibilities.append(h0_h1[0][0])
    count = 1
    while count<len(h0_h1[0]):
        new_possibilities = []
        for each in possibilities:
            new_each = copy.deepcopy(each)
            each.append(h0_h1[0][count])
            new_each.append(h0_h1[0][count])
            new_possibilities.append(each)
            new_possibilities.append(new_each)
#         print len(new_possibilities)
#         print new_possibilities
        possibilities = copy.deepcopy(new_possibilities)
#         print "len of possibilities"+ str(len(possibilities))
#         print possibilities
        count +=1
        print count
    return possibilities


 