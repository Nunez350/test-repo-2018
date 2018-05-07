import os
import sys
import getopt
import glob
import pandas as pd
from Bio import SeqIO


#parameters of the script
script_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + '/'
in_dir = script_dir
out_dir = script_dir + r"get_variable_output/"
exclude_list = ['-', 'X'] #list of garbage characters or gaps
drop_exclude = True #whether to remove positions containing values in the list
write_output = False
input_filetype = r'.alnclw'
input_files = [
    
    ]
    
#/parameters

os.chdir(script_dir)
print(os.getcwd())


def usage():
    print('see code')
    sys.exit(0)

#grab df from fafsa formated aln file
def import_data(filename, extension):
    if extension == ".alnclw":
        format = "clustal"
    os.chdir(in_dir)
    data_dict = {}
    with open(filename, "rU") as handle:
        data_list = list(SeqIO.parse(handle, format))
    for entry in data_list:
        data_dict.update({entry.id:list(entry.seq)})
    #print(data_dict)
    df = pd.DataFrame(data_dict)
    df.name = filename
    # print(df)
    return df

#return list of rows w/ variable sites
def find_variable(df, exclude_sites):
    
    #run a lambda to find var rows, append result bool to df.
    not_variable = df.apply(lambda x: len(x[-x.isnull()].unique()) == 1 , axis=1)
    not_variable.name = 'not_variable'
    df = pd.concat([not_variable, df], axis=1)
           
    var_rows = []
    for row_num in df.index:
        row = df.iloc[row_num]
        #print row.loc['variable']
        if row.loc['not_variable'] == False:
            var_rows.append(row_num)
            
    for x in exclude_sites:
        if x in var_rows:
            var_rows.remove(x)
    return var_rows

#return list of rows containing gaps, junk, whatever.
def find_exclude(df):
    #ugly way of doing this. if you don't want to exclude rows, returns empty
    if drop_exclude:
        #run lambda to find gap rows, exclude w/ regex
        exclude_char = df.apply(lambda x: x.isin(exclude_list).any(), axis=1)
        exclude_char.name = 'exclude'
        df = pd.concat([exclude_char, df], axis=1)
        
        print('gaps/indels/junk:', df['exclude'].any())
        
        excluded_rows = []
        for row_num in df.index:
            row = df.iloc[row_num]
            if row.loc['exclude']:
                excluded_rows.append(row_num)
    else: 
        excluded_rows = []
    
    return excluded_rows
    
def percent_variable(df, var_sites):
     #print(df)
     #print(var_sites)
     var_percent = (float(len(var_sites))/df.shape[0])*100
     print(df.name, ' %var:', var_percent)
     return var_percent
        
    
def concat_each_gene(data_frames):
    concat_genes = []
    for df in data_frames:
        series_each_concat = (df.sum(axis=1, skipna=False).astype(str))
        series_each_concat.name = df.name
        concat_genes.append(series_each_concat)        
    df_each_gene_concat = pd.DataFrame(index=concat_genes[0].index)
    for series in concat_genes:
        df_each_gene_concat[series.name] = series.values
        print(df_each_gene_concat)
    return df_each_gene_concat
    assert 0
    

def build_csv(df, var_sites, write_output):
    if write_output:
        os.chdir(out_dir)    
    df_var_sites = df.iloc[var_sites]
    df_var_sites = df_var_sites.transpose()
    print(df.name)
    
    df_var_sites.name = df.name    
    positions = [x+1 for x in list(df_var_sites.columns.values)]
    df_var_sites.columns = positions   
    if write_output:
        if input_filetype == ".alnclw":
            output_filename = 'df_'+df.name[:-7]+'_var.csv'
        df_var_sites.to_csv(output_filename)
        print('written to:' + out_dir + output_filename)
    else:
        print(df_var_sites)
    
        
try:
    opts, args = getopt.getopt(sys.argv[1:],"hwf:i:o:")
    print(opts)
except:
    print('arguments skipped')
for opt, arg in opts:
    if opt == '-h': #help
        usage()
    elif opt == '-w': #save output
        write_output = True
    elif opt == '-i': #input directory
        in_dir = os.path.join(script_dir, arg)
        print(in_dir)
    elif opt == '-o': #output directory, must be a subdir of current directory
        out_dir = os.path.join(script_dir, arg)
        print(out_dir)
    elif opt == "-f": #file extension
        input_filetype = arg
        
if write_output and not os.path.exists(out_dir):
    os.makedirs(out_dir)

if len(args) > 0:
    input_files = args
#uncomment this else to require input
#else:
#    usage()

#get all files with the filetype extension in the script's directory
input_files_absolute = glob.glob(in_dir + "*" + input_filetype)
for path in input_files_absolute:
    input_files.append(os.path.basename(path))
print(input_files)

for filename in input_files:
    df = import_data(filename, input_filetype)
    exclude_sites = find_exclude(df)
    var_sites = find_variable(df, exclude_sites)
    var_percent = percent_variable(df, var_sites)
    build_csv(df, var_sites, write_output)



