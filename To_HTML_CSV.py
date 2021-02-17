#!/usr/bin/env python
# coding: utf-8

# In[ ]:


save_copy.to_csv('Transition_Formatted.txt', sep='\t', index = False)
Lifetimes.to_csv('Lifetime_Formatted.txt', sep='\t', index = False)


# In[1]:


#table to be used in excel, has more error places. 
excel_copy = all_state.copy()
#drops the f states
for i in range(len(excel_copy)-1, 0, -1):
    if excel_copy.Initial[i][1] >= 3:
        excel_copy.drop(i, axis = 0, inplace = True)
excel_copy['Initial'] = save_copy['Initial']
excel_copy['Decay'] = save_copy['Decay']

#drops calculation columns
excel_copy.drop(['Ei', 'Ef', 'Ei_unc', 'Ef_unc', 'mat_werr', 'old_unc', 'n', 'l', 's'], axis = 1, inplace = True)
excel_copy.rename(columns = {'matrix': 'Matrix Element (a.u.)', 
                             'mat_unc': 'Matrix Error', 'wavelength': 'Wavelength (nm)', 'Eerr': 'Wavelength Error',
                             'transition_rate s-1': 'Transition Rate (s-1)', 'Terr': 'Transition Rate Error',
                            'branching ratio': "Branching Ratio", 'Berr': "Branching Ratio Error"}, inplace = True)
excel_copy.drop(['nf', 'lf', 'sf', 'precise_wave', 'precise_Eerr'], axis = 1, inplace = True)

#reorder to put modification after wavelength error, then rename
excel_copy = excel_copy[['Initial', 'Decay', 'Matrix Element (a.u.)', 'Matrix Error', 
       'Wavelength (nm)', 'Wavelength Error', 'modif', 'Transition Rate (s-1)',
       'Transition Rate Error', 'Branching Ratio', 'Branching Ratio Error']]
excel_copy.rename(columns = {'modif': 'Flag'}, inplace = True)


# In[ ]:


#no_errors is the version that will be shown when they click "all"

no_errors = save_copy.copy()
matrixx = []
wavell = []
transrr = []
branchh = []
for i in range(len(no_errors)):
    matrixx.append(no_errors['Matrix element (a.u.)'][i].split('(')[0])
    wavell.append(no_errors['Wavelength (nm)'][i].split('(')[0])
    transrr.append(no_errors['Transition Rate (s-1)'][i].split('(')[0] + no_errors['Transition Rate (s-1)'][i].split(')')[1])
    branchh.append(no_errors['Branching ratio'][i].split('(')[0])
no_errors['Matrix element (a.u.)'] = matrixx
no_errors['Wavelength (nm)'] = wavell
no_errors['Transition Rate (s-1)'] = transrr
no_errors['Branching ratio'] = branchh


# In[ ]:


#to get branching ratios out of scientific notation in html
Br_not_sci = [] 
Brer_not_sci = []
for i in range(len(excel_copy)):
    Br_not_sci.append(str(excel_copy['Branching Ratio'][i]))
    Brer_not_sci.append(str(excel_copy['Branching Ratio Error'][i]))
excel_copy['Branching Ratio'] = Br_not_sci
excel_copy['Branching Ratio Error'] = Brer_not_sci


# In[ ]:


#Gets rid of "Flag columns"
Flags = excel_copy['Flag']
excel_copy.drop(columns = {'Flag'}, inplace = True)


# In[ ]:


#changes to HTML tabular format
html = save_copy.to_html(index = False)
html2 = Lifetimes.to_html(index = False)
html3 = no_errors.to_html(index = False)
html4 = excel_copy.to_html(index = False)


# In[ ]:


#adds in html formatted subscripts
sub_scripts = ['1/2', '3/2', '5/2', '7/2', '9/2', '11/2']
htmls = [html, html2, html3, html4] #save_copy, Lifetimes, no_error, excel_copy
for i in sub_scripts:
    for j, k in enumerate(htmls):
        htmls[j] = htmls[j].replace('%s' % i, '<sub>%s</sub>' % i)


# In[ ]:


with open('save_copy.html', 'w') as fo:
    fo.write(htmls[0])


# In[ ]:


with open('Lifetimes.html', 'w') as fo:
    fo.write(htmls[1])


# In[ ]:


with open('no_errors.html', 'w') as fo:
    fo.write(htmls[2])


# In[ ]:


with open('excel_copy.html', 'w') as fo:
    fo.write(htmls[3])

