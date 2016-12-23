#Program to coordinate data from Gamess-uk punch file and
# output an xyz file

def convert_b_to_a(val):
    ''' Converts bohr to angstroms '''
    converted = float(val) / 1.8897161646320724 
    return converted

def convert_h_to_ev(val):
    '''Converts Hartree to eV'''
    converted = float(val) * 27.2114
    return converted

def write_outxyz(outnum,title,num_atoms,data,energy):
#Strip off the extension and create output file
    energy = convert_h_to_ev(energy)
    outfile = punfile.split(".")[0] + '_'+ outnum + '.xyz'
    out = open(outfile,'w')
    print 'Writing data to',outfile
    out.write(str(num_atoms)+'\n')
    writestr = title.rstrip() + ' SCF energy: '+ str(energy) + '\n'
    out.write(writestr)
    for i in range(int(num_atoms)):
        writestr = atomlist[i]+ ' ' 
        for num in data[i]:
            val = convert_b_to_a(num)
            writestr = writestr + str(val) + ' '
        writestr=writestr + '\n'
        out.write(writestr)
    out.close()

punfile = raw_input('Enter punch file name:  ')
try :
    pun = open(punfile,'r')
except:
    print 'Punchfile ',punfile,'not found!'
    exit()

#General variables
title = 'pun2xyz_title\n'  #Placeholder for title in case it is not in punchfile
debug = False  #Set to true to get lots of output!
energy = 0.00  # Store the scf energy
outnum = '000'  #Filename number for output file
newline='' 
line_num = 0    # A counter for the number of lines
data=list()     #List containing the data values
atomlist=list() #List for atom symbols

#Read punch file line by line
for line in pun:
    line.rstrip()  #Removes the trailing \n character
    line_num = line_num + 1
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
               title.rstrip()
               if debug: print 'The title is',title
               break 
        elif word == 'scf_energy':
            energy = 0.00
            for scf_energy in pun:
                line_num = line_num + 1
                energy = energy + float(scf_energy)
                if debug: print "The energy is",energy
                write_outxyz(outnum,title,num_atoms,data,energy)
                outnum = "{0:03d}".format(int(outnum) + 1)
                break
        elif word == 'coordinates':
            data=list()
            atomlist=list()
            num_atoms = int(words[5]) 
            if debug: print 'There are',num_atoms,'atoms'
            count = 1
            for val in pun:
                val.rstrip('\n')
                line_num = line_num + 1
                atomlist.append(val.split()[0])
                data.append(val.split()[1:4])
                if debug: 
                    print atomlist
                    print data
                count = count + 1
                if count > num_atoms: 
                    break
pun.close()
print 'Program complete.\n\n',line_num,'lines read\n\nPlease check output files\n\n\n'
############################################################################
