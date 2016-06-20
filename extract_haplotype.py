#extract haplotype
import re



def classify_file(file_name):
    file_type = []
    if re.match('.*no_error',file_name) or re.match('easy',file_name):
        file_type.append('no_error');
    elif re.match('.*with_error',file_name) or re.match('medium',file_name):
        file_type.append('with_error')
    if re.match('.*high_error', file_name):
        file_type.append('high_error')
    elif re.match('.*low_error',file_name):
        file_type.append('low_error')
   
    return file_type


def extract_haplotype(file_name):
    file_path = "/Users/qinyiyan/Dropbox/ucla/2016spring/224/proj/Final_2/" + file_name
    l = []
    with open(file_path, 'r') as in_file:
      for line in in_file:
        line = line.strip()
        #print len(line)
        if len(line) > 0:
          l.append(map(str, line.split(',')))
    
    file_type = classify_file(file_name)
    
    print file_type
    
    col_num = len(l[0][0])
    print col_num
    homo_col_index = {}
    col_hash = {}
    col_hash[0] = 0
    col_hash[1] = 0
    col_hash['total'] = 0
    
    threshold=0       
    #set threshold according to file type
    if file_type[0] == "no_error":
        threshold = 0.99
    elif file_type[0] == "with_error":
        if file_type[1] == "high_error":
            threshold = 0.7
        elif file_type[1] == "low_error":
            threshold = 0.8
    print threshold 
    
    for col in range (0,col_num):
        col_hash[0] = 0
        col_hash[1] = 0
        col_hash['total'] = 0
        for row in range(0,len(l)):
            #print l[row][col]
            if l[row][0][col] == '0':
                #print 0
                col_hash[0] = col_hash[0]+1
                col_hash['total'] = col_hash['total'] + 1
            elif l[row][0][col] == '1':
                #print 1
                col_hash[1] = col_hash[1]+1
                col_hash['total'] = col_hash['total'] + 1
        #print col_hash     
        if col_hash[0]/float(col_hash['total'])>threshold:
            homo_col_index[col] = 0
        elif col_hash[1]/float(col_hash['total'])>threshold:
            homo_col_index[col] = 1
            
    hetero_cols = [col for col in range(0,col_num) if col not in homo_col_index]
    #print hetero_cols
    #return (l, homo_col_index)
    
    data = []
    for row in l:
        for i in range(0, len(row)):
            if row[i] != '-':
                data.append(list(row[0][i] for i in hetero_cols))
        
    print len(data[0])
    return (data,homo_col_index)




def array_to_string(reads):
    string_reads = []
    for read in reads:
        read = ''.join(read)
        string_reads.append(read)
    return string_reads


