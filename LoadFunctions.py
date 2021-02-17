#!/usr/bin/env python
# coding: utf-8

# In[1]:


c_val = 2.02613 * 10**18 
def transition_rate_calc(m,j,lam): #takes in matrix element, total momentum, wavelength in cm-1
    lam = lam * 10**8 #converts to Angstrom from cm-1
    jval = 2 * j + 1 #bottom part of first half
    m2 = m**2 #matrix element squared. Will need to be variable
    lam3 = lam**3
    A = (c_val / jval) * (m2 / lam3)
    return A

def lifetime_calc(amas): #takes in list of all transition rates
    return 1/np.sum(amas)

def branching_ratio_calc(a, lifet): #takes in a transition rate
    return a*lifet


# In[2]:


def energy_err_calc(Ei, Ef, Eierr, Eferr):
    a = Ei #higher energy
    b = Ef
    err_a = Eierr
    err_b = Eferr
    return (1/(a-b)**2) * np.sqrt( (err_a)**2 + (err_b)**2 ) * 10**8 #into Angstrom from cm-1
    
def transition_err_calc(m,j,lam, merr, lamerr): #takes in matrix element, total momentum, wavelength in Angstrom
    m, j, lam, merr, lamerr = m, j, lam, merr, lamerr
    m2 = m**2 #matrix element squared. Will need to be variable
    lam = lam * 10**8 #converting to Angstrom from cm -1. Lamerr is already converted.
    lam3 = lam**3
    jval = 2 * j + 1
    return (c_val / jval) * (m2/lam3) * np.sqrt( ((m2 * 2 * merr / m) / m2)**2 + ((lam3 * 3 * lamerr / lam) / lam3)**2 )

#Look into Transition error, right number, wrong factor
def lifetime_err_calc(trs, errs): #takes in list of all transition rates
    X = np.sum(trs)
    errs = [i ** 2 for i in errs]
    return (1 / X)**2 * np.sqrt(np.sum(errs))

def lifetime_err_calc2(trs, errs): #takes in list of all transition rates
    num_trans = len(errs) #number of rates
    errs = pd.DataFrame(errs, columns = ['n', 'l', 's', 'error'])
    errs.sort_values(by=['l', 'n', 's'], ascending = [True, True, True], inplace = True)
    errs.reset_index(drop = True, inplace = True)
    X = np.sum(trs)
    direct_add = [] #holder for individual sets of correlated states
    quad_add = [] #holder for sets which add in quadrature, non-correlated
    all_corr = [] #holds all the lists of errors for correlated states
    if num_trans > 1: #multiple transitions
        for i in range(len(errs)-1):
            if errs['n'][i] == errs['n'][i+1] and errs['l'][i] == errs['l'][i+1]:
                direct_add.append(errs['error'][i])
                direct_add.append(errs['error'][i+1])
            else:
                direct_add = list(dict.fromkeys(direct_add))
                all_corr.append(direct_add)
                direct_add = []
                quad_add.append(errs['error'][i])
                quad_add.append(errs['error'][i+1])
            
        direct_add = list(dict.fromkeys(direct_add)) #remove duplicates
        all_corr.append(direct_add) #added here in case there is no "else" case
        flat_all = [item for sublist in all_corr for item in sublist] #flattened all_corraleted
        flat_all = list(dict.fromkeys(flat_all)) #remove duplicate errors
        quad_add = list(dict.fromkeys(quad_add)) #remove duplicates
        quad_add = [elem for elem in quad_add if elem not in flat_all] #removed quadratic adding elements if they should be linear

        corr_sum = [] #directly added errors of correlated values
        for i in all_corr:
            corr_sum.append(np.sum(i))
        all_errs = corr_sum + quad_add
        squares = [i**2 for i in all_errs]
        #return np.sqrt(np.sum(squares))

        return (1 / X)**2 * np.sqrt(np.sum(squares))
    else:
        error = float(errs['error'])
        return (1 / X)**2 * np.sqrt(error**2)


def branching_ratio_error(Tr, Trs, TrError, TrErrors, lifetime):
    sums = 1/lifetime #sum of all transition rates
    all_errors = []
    for i in range(len(Trs)):
        if Trs[i] == Tr:
            numer = sums - Trs[i]
            denom = sums**2
            Error1 = (numer / denom)**2
            Error1 = Error1 * (TrErrors[i]**2)
        else:
            numer = Tr
            denom = sums**2
            Error1 = (numer / denom)**2
            Error1 = Error1 * (TrErrors[i]**2)
        all_errors.append(Error1)
    Br_error = np.sqrt(np.sum(all_errors))
    if len(all_errors) == 1:
        Br_error = 0
    return Br_error


# In[3]:


def ang_to_nm(x):
    return x*(10**-1)
def cm_to_nm(x):
    return x*(10**7)
def cm_to_ang(x):
    return x*(10**8)
def s_to_ns(x):
    return x*(10**9)
def conversion(x):
    #return np.format_float_scientific(x, 3)
    return "{:.3e}".format(x)


# In[4]:


def to_one_dig(wavelength, error):
    """
    "takes in a wavelength and error and uses it to produce ####(#) format"
    "could possibly be used to do a different number of (###) digits"
    """
    wavelength = wavelength
    error = error
    original = round(wavelength, error, format = 'Drake') #number with 2 err_dig and ()
    
    og_err = pattern.findall(original)[0] #just the error if it has one
    new_err = round(og_err, sigfigs = 1)[0]
        
    og_num = original.split('(')[0] #just the number
#     except (IndexError, TypeError): #if there is no Error
#         og_err = ''
#         new_err = ''
#         og_num = original #number doesn't have ()
        
    if 'E' in original:
        err_in_paren = re.search('\(([^)]+)', original).group(1)
        og_num = str(float(original.replace('(%s)' % err_in_paren, '' ))) #gets it out of scientific notation and back into str
    new_sfigs = len(og_num.replace('.', '')) - 1 #how many digits new 1 number should have
    new_num = round(wavelength, sigfigs = new_sfigs) #number moved back one sig fig
    #print(new_num, 'nn')
    #find how many decimal spots there are
    #print(original, new_sfigs, og_num, og_num.split('.'))
    #print(og_num.split('.')[1])
    try:
        #num_deci = new_sfigs - len(og_num.split('.')[1])
        
        num_deci = len(og_num.split('.')[1]) - 1
        #print(new_sfigs, og_num, num_deci)
        #heres the problem: og_num adds 0 to the end of the number if the error is at the last digit
        #so 1359.2016, .0006 goes to 1359.20160, which if you subtract the decimals gives one number less than you want
    except IndexError:
        num_deci = new_sfigs
    #run condition to see if the wavleneght has an added '0' at end for sig_figs
#     if len(og_num.split('.')[1]) > len(str(wavelength).split('.')[1]):
#         #add one since we don't want to include that in sig fig calc
#         num_deci += 1
    deci_format = "%%.%sf" % num_deci
    new_num = deci_format % new_num
    #print(original, 'original', og_num, 'og_num', new_num, 'new_num2', deci_format)
    #print(og_err, new_err)
    #print('errors', error, og_err, new_err)
    
    #new_num = str("")
    #if you want to use scientific notation, keep original as round(wavelength, error, format = 'Drake')

    final_value = new_num + '(' + new_err + ')'
    if float(error) == 0:
        final_value = wavelength
    return final_value


# In[5]:


def to_one_dig_small(wavelength, error):
    """
    "takes in a wavelength and error and uses it to produce ####(#) format"
    "could possibly be used to do a different number of (###) digits"
    """
    wavelength = wavelength
    error = error
    original = round(wavelength, error, format = 'Drake') #number with 2 err_dig and ()
    
    og_err = pattern.findall(original)[0] #just the error if it has one
    new_err = round(og_err, sigfigs = 1)[0]
        
    og_num = original.split('(')[0] #just the number
#     except (IndexError, TypeError): #if there is no Error
#         og_err = ''
#         new_err = ''
#         og_num = original #number doesn't have ()
        
    if 'E' in original:
        err_in_paren = re.search('\(([^)]+)', original).group(1)
        og_num = str(float(original.replace('(%s)' % err_in_paren, '' ))) #gets it out of scientific notation and back into str
    new_sfigs = len(og_num.replace('.', '')) - 1 #how many digits new 1 number should have
    new_num = round(wavelength, sigfigs = new_sfigs) #number moved back one sig fig
    #print(new_num, 'nn')
    #find how many decimal spots there are
    #print(original, new_sfigs, og_num, og_num.split('.'))
    #print(og_num.split('.')[1])
    try:
        #num_deci = new_sfigs - len(og_num.split('.')[1])
        
        num_deci = len(og_num.split('.')[1]) - 1
        #print(new_sfigs, og_num, num_deci)
        #heres the problem: og_num adds 0 to the end of the number if the error is at the last digit
        #so 1359.2016, .0006 goes to 1359.20160, which if you subtract the decimals gives one number less than you want
    except IndexError:
        num_deci = new_sfigs
    #run condition to see if the wavleneght has an added '0' at end for sig_figs
#     if len(og_num.split('.')[1]) > len(str(wavelength).split('.')[1]):
#         #add one since we don't want to include that in sig fig calc
#         num_deci += 1
    deci_format = "%%.%sf" % num_deci
    new_num = deci_format % new_num
    #print(original, 'original', og_num, 'og_num', new_num, 'new_num2', deci_format)
    #print(og_err, new_err)
    #print('errors', error, og_err, new_err)
    
    #new_num = str("")
    #if you want to use scientific notation, keep original as round(wavelength, error, format = 'Drake')
    #print(('%.1g' % error)[-1])
    one_dig_error = ('%.1g' % error)[-1]
    final_value = new_num + '(' + one_dig_error + ')'
    if float(error) == 0 or float(error) < .0001:
        final_value = '%.4f' % wavelength #always 4 decimals 
    return final_value

