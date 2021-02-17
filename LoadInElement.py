#!/usr/bin/env python
# coding: utf-8

# In[1]:



#Read in file paths based on element name as it is saved. 
#Verify skiprows for each element


# In[2]:


#%run -i LoadFunctions.py


# In[3]:


import numpy as np
import pandas as pd
from fractions import Fraction
import xlsxwriter
import decimal
from decimal import *
import re
from modsigfig import round #does this need to be done 
pd.set_option('display.max_rows', 500)
getcontext().prec = 20


# In[4]:

try: element
except NameError: element = input('Element name in files:')
# element = input('Element name in files:')
skiprows_data = 0 #for database
skiprows_mats = 1 #for datapol
dataname = "Data\%s\database%s.txt" % (element,element) #used in getting (#) format of erros
matname = "Data\%s\datapol%s.txt" % (element, element) #the rest of the data
checkratesname = "Data\\%s\\rates1.txt" % element
checklifesname = "Data\\%s\\rates2.txt" % element


# In[5]:


#Reads in data


# In[6]:


database = pd.read_csv(dataname, sep = '\s+', engine = 'python', header = None, skiprows = skiprows_data)
real_mats = []
for d, i in enumerate(database[5]):
    if i == None:
        real_mats.append(database[4][d])
    else:
        real_mats.append(i)
database[5] = real_mats
database.drop(columns = [0,1,2,3,4], inplace = True)
database
columns = ['matrix']
database.columns = columns
database[['matrix', 'unc']] = database['matrix'].str.split('(', expand = True)
database[['unc', 'trash']] = database['unc'].str.split(')', expand = True)
database.drop('trash',axis = 1, inplace = True)

#have to read in as str or else pandas does weird rounding. Convert numbers back to float after
ele = pd.read_csv(matname, sep = '\s+', engine = 'python', header = None, skiprows = skiprows_mats, dtype = 'str')
cutoff_index = ele[ele[1].isnull()].index[0]
mats = ele[:cutoff_index]
energies = ele[cutoff_index+1:]

columns = ['start', 'end','matrix', 'unc']
mats.columns = columns
mats['old_unc'] = database['unc']
columns2 = ['level', 'ene', 'unc', 'modif' ]
energies.columns = columns2
energies.reset_index(inplace = True, drop = True)
mats.reset_index(inplace = True,drop = True)


# In[7]:


#Gets start states


# In[8]:


#Processing of mats file off of end state, since ground state will not decay
#creates dataframe of all possible beginning states
def split(word): 
    return list(word) 

all_names = []
#splits the original n+l number into components
for i in mats['end']:
    nm = split(i)
    name = [string for string in nm if string != " "]
    all_names.append(name)

# fg_hold = []
# for i in range(len(all_names)):
#     if 'f' in all_names[i]: 
#         #print(all_names[i])
#         fg_hold.append(i)
   
# all_names = np.delete(all_names, fg_hold).tolist()
#changes s, p, d into 0, 1, 2
for i in all_names:
    if 's' in i:
        i[i.index('s')] = 0
    elif 'p' in i:
        i[i.index('p')] = 1
    elif 'd' in i:
        i[i.index('d')] = 2
    elif 'f' in i:
        i[i.index('f')] = 3
    elif 'g' in i:
        i[i.index('g')] = 4
    
#changes n element into integer, whether its 1 or 2 digits
for i in all_names:
    if isinstance(i[1], str): #means it hasnt been changed to 0,1,2 which means its a 2 digit n value. i.e. 12
        i[0] = int(i[0] + i[1])
        del i[1]
    else:
        i[0] = int(i[0])

#converts last 3 numbers into 1 j value
for i in all_names:
    i[2] = int(i[2]) / int(i[4])
    del i[4]
    del i[3]

#adds back in matrix elements and uncertainty, starts column titles
for count, i in enumerate(all_names):
    i.append(mats.matrix[count])
    i.append(mats.unc[count])
columns = ['n','l','j','m','unc']
ends = pd.DataFrame(all_names, columns=columns)


# In[9]:


#gets decay state values


# In[10]:


#Processing of mats file off of start state,
#creates dataframe of some decay states. Not all of them, as n is not included

all_names = []
#splits the original n+l number into components
for i in mats['start']:
    nm = split(i)
    name = [string for string in nm if string != " "]
    all_names.append(name)
 

#changes s, p, d into 0, 1, 2
for i in all_names:
    if 's' in i:
        i[i.index('s')] = 0
    elif 'p' in i:
        i[i.index('p')] = 1
    elif 'd' in i:
        i[i.index('d')] = 2
    elif 'f' in i:
        i[i.index('f')] = 3
    elif 'g' in i:
        i[i.index('g')] = 4

#changes n element into integer, whether its 1 or 2 digits
for i in all_names:
    if isinstance(i[1], str): #means it hasnt been changed to 0,1,2 which means its a 2 digit n value. i.e. 12
        i[0] = int(i[0] + i[1])
        del i[1]
    else:
        i[0] = int(i[0])

#converts last 3 numbers into 1 j value
for i in all_names:
    i[2] = int(i[2]) / int(i[4])
    del i[4]
    del i[3]

#adds back in matrix elements and uncertainty, starts column titles
for count, i in enumerate(all_names):
    i.append(mats.matrix[count])
    i.append(mats.unc[count])
columns = ['n','l','j','m','unc']
starts = pd.DataFrame(all_names, columns=columns)


# In[11]:


#gets energy values


# In[12]:


all_names = []
#splits the original n+l number into components
for i in energies['level']:
    nm = split(i)
    name = [string for string in nm if string != " "]
    all_names.append(name)
 

#changes s, p, d into 0, 1, 2
for i in all_names:
    if 's' in i:
        i[i.index('s')] = 0
    elif 'p' in i:
        i[i.index('p')] = 1
    elif 'd' in i:
        i[i.index('d')] = 2
    elif 'f' in i:
        i[i.index('f')] = 3
    elif 'g' in i:
        i[i.index('g')] = 4

#changes n element into integer, whether its 1 or 2 digits
for i in all_names:
    if isinstance(i[1], str): #means it hasnt been changed to 0,1,2 which means its a 2 digit n value. i.e. 12
        i[0] = int(i[0] + i[1])
        del i[1]
    else:
        i[0] = int(i[0])

#converts last 3 numbers into 1 j value
for i in all_names:
    i[2] = int(i[2]) / int(i[4])
    del i[4]
    del i[3]

#adds back in matrix elements and uncertainty, starts column titles
for count, i in enumerate(all_names):
    i.append(energies.ene[count])
    i.append(energies.unc[count])
    i.append(energies.modif[count])
columns = ['n','l','j','ene','unc','modif']
n_ene = pd.DataFrame(all_names, columns=columns)
nist = n_ene.copy()


# In[13]:


#combines starts, decays and energies into one dataframe "all_state"


# In[14]:


Initial_en = []
Final_en = []
Initial_unc = []
Final_unc = []
decay = []
hold = []
for i in range(len(starts)):
    for j in range(len(nist)):
        if starts['n'][i] == nist['n'][j] and starts['j'][i] == nist['j'][j] and starts['l'][i] == nist['l'][j]:
            Initial_en.append(nist['ene'][j])
            Initial_unc.append(nist['unc'][j])
            hold.append([[starts['n'][i],starts['l'][i],starts['j'][i]], starts['m'][i], starts['unc'][i],
                         [ends['n'][i], ends['l'][i], ends['j'][i]],
                         nist['ene'][j],nist['unc'][j]])
        elif ends['n'][i] == nist['n'][j] and ends['j'][i] == nist['j'][j] and ends['l'][i] == nist['l'][j]:
            Final_en.append(nist['ene'][j])
            Final_unc.append(nist['unc'][j])
hold = pd.DataFrame(hold, columns = ['Initial', 'matrix', 'mat_unc', 'Decay', 'Ei', 'Ei_unc'])
hold['Ef'] = Final_en
hold['Ef_unc'] = Final_unc
columns = ['Initial', 'Decay', 'matrix', 'Ei', 'Ef', 'mat_unc', 'Ei_unc', 'Ef_unc']
all_state = hold[columns]

# unc_hold = []
# for i in all_state['Ef_unc']:
#     unc_hold.append("{:.2e}".format(i))
# all_state['Ef_unc'] = unc_hold
all_state['old_unc'] = database['unc']


# In[15]:


mod_hold = []
for i in range(len(all_state)):
    mod_initial = nist[(nist['n'] == all_state.Initial[i][0]) & (nist['l'] == all_state.Initial[i][1]) & (nist['j'] == all_state.Initial[i][2])]['modif'].values[0]
    mod_final = nist[(nist['n'] == all_state.Decay[i][0]) & (nist['l'] == all_state.Decay[i][1]) & (nist['j'] == all_state.Decay[i][2])]['modif'].values[0]
    mod_hold.append((mod_initial, mod_final))
    
all_state['modif'] = ''
for i in range(len(mod_hold)):
    if '*' in mod_hold[i]:
        all_state.loc[i, 'modif'] = '*'
    #mod_final = 


# In[16]:


all_state[all_state.modif == '*']


# In[17]:


#puts higher energy in Initial, sorts by energy
#does not sort decay states FIX?


# In[18]:


eis = []
efs = []
inits = []
decs = []
eis_unc = []
efs_unc = []
flipped_mat = []
for i in range(len(all_state)):
    if float(all_state.Ei[i]) < float(all_state.Ef[i]): #if we need to switch
        a = all_state.Ef[i]
        b = all_state.Ei[i]
        unc1 = all_state.Ef_unc[i]
        unc2 = all_state.Ei_unc[i]
        c2 = all_state.Decay[i]
        d = all_state.Initial[i]
        eis.append(a)
        eis_unc.append(unc1)
        efs.append(b)
        efs_unc.append(unc2)
        inits.append(c2)
        decs.append(d)
        flipped_mat.append((all_state['matrix'][i]))

    else:
        a = all_state.Ei[i]
        b = all_state.Ef[i]
        unc1 = all_state.Ei_unc[i]
        unc2 = all_state.Ef_unc[i]
        c2 = all_state.Initial[i]
        d = all_state.Decay[i]
        eis.append(a)
        eis_unc.append(unc1)
        efs.append(b)
        efs_unc.append(unc2)
        inits.append(c2)
        decs.append(d)
        #print(unc1)
        
all_state['Initial'] = inits
all_state['Decay'] = decs
all_state['Ei'] = eis
all_state['Ef'] = efs
all_state['Ei_unc'] = eis_unc
all_state['Ef_unc'] = efs_unc
#mat_page = all_state.copy()
#mat_page.reset_index(inplace = True, drop = True)
all_state.sort_values('Ei', inplace = True)
all_state.reset_index(inplace = True, drop = True)
#HERE IS ORDERING?


# In[19]:


#indices of all spots where the ordering of the states was flipped
flipped_ind = []
for i in range(len(flipped_mat)):
    indx = np.where(all_state.matrix == flipped_mat[i])[0][0]
    flipped_ind.append(indx)


# In[20]:


#old code that checked for duplicate values


# In[21]:


initial_holds = list(all_state.Initial)
ends_holds = list(all_state.Decay)
mat_holds = list(all_state.matrix)
dups = []
for k, i in enumerate(all_state.matrix):
    ms = all_state.matrix[k]
    ini = all_state.Initial[k]
    end = all_state.Decay[k]
    res_list = [i for i in range(len(mat_holds)) if (mat_holds[i] == ms) 
                and (initial_holds[i] == ini) and (ends_holds[i] == end)]
    if len(res_list) > 1:
        dups.append(res_list[1:])
dups


# In[22]:


#Removes duplicates, resets index. 
if len(dups) != 0:
    dups = pd.DataFrame(dups)
    dups.drop_duplicates(inplace = True)
    dups = list(dups[0])
    all_state.drop(index = dups, inplace = True)
    all_state.reset_index(inplace = True, drop = True)
    all_state['matrix'] = pd.to_numeric(all_state.matrix)


# In[23]:


#replaces Nan with 0 values in uncertainty, changes energy, matrix and their errors to strings then to Decimals
###############possibly source of precision loss##########################


# In[24]:


all_state['Ef_unc'].fillna(0, inplace = True)
Ef_uncs = []
for i in all_state.Ef_unc:
    #print(i)
    if i == 'nan':
        Ef_uncs.append(0)
    else:
        Ef_uncs.append(i)
#     try: 
#         if np.isnan(i) == True or i == 'nan':
#             print(i)
#     except TypeError:
#         if i == 'nan':
            #print(i)

all_state.Ef_unc = Ef_uncs
all_state.Ei = all_state.Ei.apply(str).apply(Decimal)
all_state.Ef = all_state.Ef.apply(str).apply(Decimal)
all_state.Ei_unc = all_state.Ei_unc.apply(str).apply(Decimal)
all_state.Ef_unc = all_state.Ef_unc.apply(str).apply(Decimal)
all_state.mat_unc = all_state.mat_unc.apply(str).apply(Decimal)
all_state.matrix = all_state.matrix.apply(str).apply(Decimal)


# In[25]:


all_state[233:234]


# In[26]:


#creates new column mat_werr that has the matrix plus (#) format of error in one column
mat_werr = []
for i in range(len(all_state)):
    try:
        mat_werr.append(round(str(all_state.matrix[i]), str(all_state.mat_unc[i]), format = 'Drake'))
    except ValueError:
        print(i)
all_state['mat_werr'] = mat_werr


# In[27]:


#changes nls format to list to order correctly
old_state = all_state.copy() #version before ordering
all_state[['n','l', 's']] = pd.DataFrame(all_state.Initial.tolist(), index= all_state.index)
all_state[['nf','lf', 'sf']] = pd.DataFrame(all_state.Decay.tolist(), index= all_state.index)
all_state.sort_values(by=['l', 'n', 's','nf', 'lf', 'sf'], ascending = [True, True, True, True, True, True], inplace = True)
all_state.reset_index(drop = True, inplace = True)


# In[28]:


#creates new all_state columns with Initial, Decay in '7s1/2' format
from sympy import pretty_print as pp, latex
from sympy import Symbol

ini_hold = []
dec_hold = []
n_holdI, l_holdI, s_holdI = [], [], []
n_holdD, l_holdD, s_holdD = [], [], []
for i in range(len(all_state)):
    #Initial
    n = str(all_state.Initial[i][0])
    if all_state.Initial[i][1] == 0:
        l = 's'
    elif all_state.Initial[i][1] == 1:
        l = 'p'
    elif all_state.Initial[i][1] == 2:
        l = 'd'
    elif all_state.Initial[i][1] == 3:
        l = 'f'
    if all_state.Initial[i][2] == 0.5:
        s = '1/2'
    elif all_state.Initial[i][2] == 1.5:
        s = '3/2'
    elif all_state.Initial[i][2] == 2.5:
        s = '5/2'
    elif all_state.Initial[i][2] == 3.5:
        s = '7/2'
    elif all_state.Initial[i][2] == 4.5:
        s = '9/2'
    ini = n+l+s
    ini_hold.append(ini)
    n_holdI.append(n)
    l_holdI.append(l)
    s_holdI.append(s)
    
    #Decay
    n = str(all_state.Decay[i][0])
    if all_state.Decay[i][1] == 0:
        l = 's'
    elif all_state.Decay[i][1] == 1:
        l = 'p'
    elif all_state.Decay[i][1] == 2:
        l = 'd'
    elif all_state.Decay[i][1] == 3:
        l = 'f'
    if all_state.Decay[i][2] == 0.5:
        s = '1/2'
    elif all_state.Decay[i][2] == 1.5:
        s = '3/2'
    elif all_state.Decay[i][2] == 2.5:
        s = '5/2'
    elif all_state.Decay[i][2] == 3.5:
        s = '7/2'
    elif all_state.Decay[i][2] == 4.5:
        s = '9/2'
    dec = n+l+s
    dec_hold.append(dec)
    n_holdD.append(n)
    l_holdD.append(l)
    s_holdD.append(s)
    
all_state['Initial_form'] = ini_hold #formatted 
all_state['Decay_form'] = dec_hold


# In[29]:


#puts in the experimental matrix values into all_state in matrix, uncertainty, and combined () format
#has to run for loop twice because experimental data are not ordered in Initial Decay format, Decay may be first
if 'II' in element:
    #number of ionizations
    element_othernm = element.split('I')[0] + '+' * (len(element.split('I')) - 2)
    exp_data_name = "Experimental_Data\\%s-matrix-elements.csv" % element_othernm
else:
    exp_data_name = "Experimental_Data\\%s-matrix-elements.csv" % element


# In[30]:


#indices of all spots where the ordering of the states was flipped
flipped_ind = []
for i in range(len(flipped_mat)):
    indx = np.where(all_state.matrix == Decimal(flipped_mat[i]))[0][0]
    flipped_ind.append(indx)


# In[31]:


#reads in experimental data
try:
    exp = pd.read_csv(exp_data_name) #experiment
    a = list(all_state.Initial_form)
    b = list(all_state.Decay_form)
    c = list(zip(a,b))

    d = list(exp.From)
    e = list(exp.To)
    f = list(zip(d,e))
    replaced_ind = []
    print('Replaced Values, experimental index, all_state index')
    for i in range(len(f)):
        try:
            l = np.where((all_state['Initial_form'] == f[i][1]) & (all_state['Decay_form'] == f[i][0]))[0][0]
            all_state.iloc[l, all_state.columns.get_loc('matrix')] = exp['value'][i]
            all_state.iloc[l, all_state.columns.get_loc('mat_unc')] = exp['uncertainity'][i]
            all_state.iloc[l, all_state.columns.get_loc('mat_werr')] = exp['Matrixelement'][i] + exp['Ref'][i]
            replaced_ind.append(l)
            print(i, l)
        except IndexError:
            pass
    for i in range(len(f)):
        try:
            l = np.where((all_state['Initial_form'] == f[i][0]) & (all_state['Decay_form'] == f[i][1]))[0][0]
            all_state.iloc[l, all_state.columns.get_loc('matrix')] = exp['value'][i]
            all_state.iloc[l, all_state.columns.get_loc('mat_unc')] = exp['uncertainity'][i]
            all_state.iloc[l, all_state.columns.get_loc('mat_werr')] = exp['Matrixelement'][i] + exp['Ref'][i]
            replaced_ind.append(l)
            print(i, l)
        except IndexError:
            pass
except FileNotFoundError:
    pass


# In[32]:


all_state.drop(['Initial_form', 'Decay_form'], axis = 1, inplace = True)


# In[33]:


#Creates Transition Rates, Lifetimes, Branching ratios, and errors
#lifetimes put into new array
#changes wavelengths to nm, t_rates are in s-1


# In[34]:


states = list(all_state.Initial)
MatrixErrors, WavelengthsCm, WavelengthsUncAng, TransitionRates = [], [], [], []
TransitionRateErrors, TransitionsForLifetime, TerrorsForLifetime, Lifetimes, LifetimeErrors = [], [], [], [], []
BranchingRatios, BranchingRatioErrors = [], []
for i in range(len(all_state)):
    Ei = all_state.Ei[i]
    Ef = all_state.Ef[i]
    Eierr = all_state.Ei_unc[i]
    Eferr = all_state.Ef_unc[i]

    m = float(all_state.matrix[i])
    j = float(all_state.Initial[i][2])
    lam = float(1 / (Ei - Ef))

    #d = decimal.Decimal(str(all_state.matrix[i])) #how many decimals spots to go out to
    #d = -1 * d.as_tuple().exponent
    #merr = all_state.mat_unc[i] / (10 ** d)
    merr = float(all_state.mat_unc[i])
    
    lamerr = float(energy_err_calc(Ei, Ef, Eierr, Eferr))
    TR = transition_rate_calc(m,j,lam)
    
    TRerr = transition_err_calc(m,j,lam,merr,lamerr)
    
    MatrixErrors.append(merr)

    WavelengthsCm.append(lam)
    WavelengthsUncAng.append(lamerr)

    TransitionRates.append(TR)
    TransitionRateErrors.append(TRerr)
    
    n_dec = all_state.Decay[i][0]
    l_dec = all_state.Decay[i][1]
    s_dec = all_state.Decay[i][2]
    TransitionsForLifetime.append(TR)
    TerrorsForLifetime.append((n_dec, l_dec, s_dec, TRerr))
    
    try:
        if all_state.Initial[i] not in states[i+1:]: #If next state NOT have same Initial State Name as the current one, i.e. new transition
            Lftime = lifetime_calc(TransitionsForLifetime)
            LftimeError = lifetime_err_calc2(TransitionsForLifetime, TerrorsForLifetime)
            
            Lifetimes.append((all_state.Initial[i], Lftime, LftimeError))
            for i in range(0, len(TransitionsForLifetime)): #all the transitions
                
                BR = branching_ratio_calc(TransitionsForLifetime[i], Lftime)
                BRerr = branching_ratio_error(TransitionsForLifetime[i], TransitionsForLifetime, 
                                                  TerrorsForLifetime[i][3], [trerr[3] for trerr in TerrorsForLifetime], Lftime)
                BranchingRatios.append(BR)
                BranchingRatioErrors.append(BRerr)
                
                
            TransitionsForLifetime = []
            TerrorsForLifetime = [] #reset for next initial state
    except KeyError:
        print(i)
        
all_state['wavelength'] = WavelengthsCm
all_state.wavelength = all_state.wavelength.apply(cm_to_nm)
all_state['Eerr'] = WavelengthsUncAng
all_state.Eerr = all_state.Eerr.apply(ang_to_nm)
all_state['transition_rate s-1'] = TransitionRates
all_state['Terr'] = TransitionRateErrors
all_state['branching ratio'] = BranchingRatios
all_state['Berr'] = BranchingRatioErrors
life_linear = Lifetimes.copy()
all_linear = all_state.copy()


# In[ ]:


# def branching_ratio_error(Tr, Trs, TrError, TrErrors, lifetime):
#     sums = 1/lifetime #sum of all transition rates
#     all_errors = []
#     for i in range(len(Trs)):
#         #if the transition rate is for the transition we are calculating branching ratio for
#         if Trs[i] == Tr:
#             numer = sums - Trs[i] #top is All transition rates - TR of interest
#             denom = sums**2 #denom is all transition rates
#             Error1 = (numer / denom)**2 # ((sum - TR) / (sum**2)) ** 2
#             Error1 = Error1 * (TrErrors[i]**2) #Error1 * errors for this transition rate **2
#         else:
#             numer = Tr
#             denom = sums**2
#             Error1 = (numer / denom)**2
#             Error1 = Error1 * (TrErrors[i]**2)
#         all_errors.append(Error1)
#     Br_error = np.sqrt(np.sum(all_errors))
#     if len(all_errors) == 1:
#         Br_error = 0
#     return Br_error


# In[ ]:


#makes 20 decimal float approximations of wavelenght and error for "exact" calculation


# In[ ]:


precise_wave = []
precise_Eerr = []
for i in range(len(all_state)): #saves new columns of all_state to be used in calculation, that aren't rounded yet
    precise_wave.append((1/(all_state.Ei[i] - all_state.Ef[i]))*10**7)
    precise_Eerr.append(Decimal(all_state.Eerr[i]))
all_state['precise_wave'] = precise_wave
all_state['precise_Eerr'] = precise_Eerr


# In[ ]:


#saves the wavelength and its error with the same number of digits past the decimal as the original initial energy had
new_wavelength = []
new_wave_error = []
for p in range(len(all_state)):
    getcontext().prec = 10
    num_digits = len(str(all_state.Ei[p]).split('.')[1]) #how many digits past the decimal spot
    new_wavelength.append(round(str(all_state.wavelength[p]), decimals = num_digits))
    new_wave_error.append(round(str(all_state.Eerr[p]), decimals = num_digits))

all_state['wavelength'] = new_wavelength
all_state['Eerr'] = new_wave_error


# In[ ]:


all_state.columns


# In[ ]:


#mat_page is what is going to be stored in matrix elements page
mat_page = all_state.copy()
mat_page

flipped_cols = [('Initial', 'Decay'), ('Ei', 'Ef'), ('Ei_unc', 'Ef_unc')]
for i in flipped_cols:
    mat_page.loc[flipped_ind,i[0]] = all_state.loc[flipped_ind, i[1]]
    mat_page.loc[flipped_ind, i[1]] = all_state.loc[flipped_ind, i[0]]

#reorder
mat_page[['n','l', 's']] = pd.DataFrame(mat_page.Initial.tolist(), index= mat_page.index)
mat_page[['nf','lf', 'sf']] = pd.DataFrame(mat_page.Decay.tolist(), index= mat_page.index)
mat_page.sort_values(by=['l', 'n', 's','nf', 'lf', 'sf'], ascending = [True, True, True, True, True, True], inplace = True)
mat_page.reset_index(drop = True, inplace = True)


# In[ ]:


mat_page

