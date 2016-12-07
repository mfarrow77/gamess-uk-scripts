#Program to read density data from Gamess-uk punch file and
# output a grid file

def convert_b_to_a(val):
    ''' Converts bohr to angstroms '''
    converted = float(val) / 1.8897161646320724 
    return converted

def write_outfile(outnum,punfile,title,points,data):
#Strip off the extension and create output file
    outfile = punfile.split(".")[0] + '_' + outnum + '.grd'
    out = open(outfile,'w')
    print 'Writing data to',outfile
    out.write(title)
    out.write('(1p,e12.5)\n')
    vals=''
    vals = vals + str(convert_b_to_a(box[0])) + ' ' + str(convert_b_to_a(box[1])) + ' ' + str(convert_b_to_a(box[2])) + ' 90.00 90.00 90.00\n'
    out.write(vals)
    vals = str(points[0]-1) + ' ' + str(points[1]-1) + ' ' + str(points[2]-1) + ' \n'
    out.write(vals)
    rnge_min = int(min(points)) / -2 
    rnge_max = int(max(points)) / 2 
    vals = '1 ' 
    for i in range(3):
        vals=vals + str(rnge_min) + ' ' + str(rnge_max-1) + ' '
    vals = vals + '\n'
    out.write(vals)
    for i in data:
        out.write(str(float(i)) +'\n')
    out.close()

punfile = raw_input('Enter punch file name:  ')
if len(punfile) < 1 : punfile = 'sample.pun'
try :
    pun = open(punfile,'r')
except:
    print 'Punchfile ',punfile,'not found!'
    exit()

#General variables
debug = False  #Set to true to get lots of output!
outnum = '000' #Filename number for output file
newline=''     #A blank string to hold the continuation line
line_num =0    # A counter for the number of lines
data=list()    #List containing the data values
mapping=list() #List containing the mapping data

#Read punch file line by line
for line in pun:
    line.rstrip()  #Removes the trailing \n character
    line_num = line_num + 1
    if debug: print line_num,line
    if len(newline) > 0 : # Check to see if this line is a continuation line
        line = newline.split('\\')[0] + line #Add old line less \ character to continuation line
        if debug: print 'Joined line:',line
        newline=''  #Dont forget to reset the continuation check!
    if not line.startswith('block') : continue
    words = line.split()
    if words[len(words)-1] == '\\': 
        if debug: print 'continuation line detected!'
        newline = line
        continue
    for word in words:
        if word == 'title':
           for title in pun:
               line_num = line_num + 1
               if debug: print 'The title is',title
               break 
        elif word == 'grid_axes':
            count = 0
            points=list()
            box=list()
            for axes in pun:
                line_num = line_num + 1
                points.append(int(axes.split()[0]))
                box.append(axes.split()[2])
                count = count + 1
                if count > 2: 
                    if debug: print points
                    break
        elif word == 'grid_mapping':
            num_map = int(words[5]) 
            if debug: print 'There are',num_map,'mapping lines'
            count = 1
            for val in pun:
                val.rstrip('\n')
                line_num = line_num + 1
                mapping.append(val)
                count = count + 1
                if count > num_map: 
                    if debug:print "mapping:",mapping
                    break
        elif word == 'grid_data':
            num_vals = words[5]
            if debug: print 'There are',num_vals,'data points'
            count =1
            data = list()
            for val in pun: 
                val.rstrip()
                line_num = line_num + 1
                data.append(val) 
                count = count +1
                if count > int(num_vals) : break
            write_outfile(outnum,punfile,title,points,data)
            outnum = "{0:03d}".format(int(outnum) + 1)
pun.close()
print 'Program complete.\n\n',line_num,'lines read\n\nPlease check output files\n\n\n'
############################################################################
#End of data loops
