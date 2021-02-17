#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import re


# In[2]:


# #read in variables
#element = 'SrII'
# #element = 'Cs'
# #element = "CaII"


# In[3]:


excel_fname = r"C:\Users\dmgame\Documents\SafronovaResearch\LifetimesWebsite\OtherData\KEY-hyperfine.xlsx"
ref_exl = pd.read_excel(excel_fname, 
                    engine='openpyxl', header = None, names = ['Ref', 'Name'])


# In[4]:


#element = "CaII"
meta_all_fname = r"C:\Users\dmgame\Documents\SafronovaResearch\LifetimesWebsite\OtherData\Metastable_elements.txt"
meta_all = pd.read_csv(meta_all_fname, engine='python', header = None, names = ['element'])
metastable_elements = list(meta_all['element'])

if element in metastable_elements:
    meta_fname = r"C:\Users\dmgame\Documents\SafronovaResearch\LifetimesWebsite\OtherData\%s_Metastable.xlsx" % (element)
    metastable = pd.read_excel(meta_fname, engine='openpyxl', skiprows = [0,1,2])
else:
    print('no metastable state')
    metastable = ''


# In[5]:


if element in metastable_elements:
    metastable_states = [] #names of states
    for i in metastable.iloc[:, 0]: #first column of metastable
        if i == i and i not in metastable_states: #not a nan value
            metastable_states.append(i)
    sub_scripts = ['1/2', '3/2', '5/2', '7/2', '9/2', '11/2']
    for i in sub_scripts:
        for j, k in enumerate(metastable_states):
            metastable_states[j] = metastable_states[j].replace('%s' % i, '<sub>%s</sub>' % i)


# In[6]:


#set up key file with refs
doi_holder = []
name_holder = []
for i in range(len(ref_exl)):
    try:
        doi_name = 'DOI' + ref_exl['Name'][i].split('DOI')[1]
    except IndexError:
        doi_name = ''
    doi_holder.append(doi_name)
    name_str = ref_exl['Name'][i].split('DOI')[0]
    last_comma = name_str.rfind(',')#finds last comma
    name_holder.append(name_str[:last_comma]) #removes last comma
ref_exl['DOI'] = doi_holder
ref_exl['Name'] = name_holder
ref_exl


# In[7]:


element_noI = element.split('I')[0]
nuclear_fname = r"C:\Users\dmgame\Documents\SafronovaResearch\LifetimesWebsite\OtherData\Nuclear-data.xlsx"
nuclear = pd.read_excel(nuclear_fname, 
                    engine='openpyxl', skiprows = [0,1,2,3,4], nrows = 82, usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14], dtype = 'str')
nuc_sub = nuclear[nuclear['Atom'] == element_noI]
nuc_sub.reset_index(inplace = True, drop = True)


# In[8]:


#find x106 etc. values in half-life, replace with superscript html tags
for i in nuc_sub.index:
    if 'x' in  nuc_sub['Half-life Ref. [1]'][i]:
        #has sig fig incorrectly applied
        faulty = nuc_sub['Half-life Ref. [1]'][i]
        corrected = faulty.split(' ')[0]
        fault_unit = ' ' + faulty.split(' ')[1]
        corrected = corrected.split('10', 1)[0] + '10' + '<sup>' + corrected.split('10', 1)[1] + '</sup>' + fault_unit
        nuc_sub.loc[i,'Half-life Ref. [1]'] = corrected
nuc_sub


# In[9]:


with open(r"C:\Users\dmgame\Documents\SafronovaResearch\LifetimesWebsite\Format_csvs\OtherData\Intro_to_nuclear.txt", encoding="utf8") as file:
    format_hold_intro = file.read()


# In[10]:


with open(r"C:\Users\dmgame\Documents\SafronovaResearch\LifetimesWebsite\Format_csvs\OtherData\Nuclear_to_hyperfine.txt", encoding="utf8") as file:
    format_hold_hyp = file.read()


# In[11]:


with open(r"C:\Users\dmgame\Documents\SafronovaResearch\LifetimesWebsite\Format_csvs\OtherData\Hyperfine_to_metastable1.txt", encoding="utf8") as file:
    format_hold_met1 = file.read()


# In[12]:


with open(r"C:\Users\dmgame\Documents\SafronovaResearch\LifetimesWebsite\Format_csvs\OtherData\Metastable1_to_2.txt", encoding="utf8") as file:
    format_hold_met2 = file.read()


# In[13]:


with open(r"C:\Users\dmgame\Documents\SafronovaResearch\LifetimesWebsite\Format_csvs\OtherData\End_formatting.txt", encoding="utf8") as file:
    format_hold_end = file.read()


# In[14]:


nist_urls = pd.read_csv(r"C:\Users\dmgame\Documents\SafronovaResearch\LifetimesWebsite\Data\nist_urls.csv",
                        header = None, names = ["Element", "URL"], index_col = 0)


# In[15]:


#the active tag of the top menu is currently on {key} is removed
key = 'Fr' #the last element to have the modfications done, so what needs to be replaced for the others
key_no_I = key.strip('I')

num_ion_key = key.count('I')
if num_ion_key == 0: #Li should be Li I
    num_ion_key += 1
num_ion_key = num_ion_key * 'I'


##Dropdown1
if 'I' in key: #this ONLY works when + is the only option
    plus_versKey = key.split('I')[0] + '+' * (len(key.split('I')) - 2)
    str1 = f'<a class="dropdown-item active" href="{key}Other.html">{plus_versKey}</a>'
    rep1 = f'<a class="dropdown-item" href="{key}Other.html">{plus_versKey}</a>'
else:
    str1 = f'<a class="dropdown-item active" href="{key}Other.html">{key}</a>'
    rep1 = f'<a class="dropdown-item" href="{key}Other.html">{key}</a>'
ind1 = format_hold_intro.find(str1)

##excel filename
stra = f"filename: '{key}OtherData',"
repa = f"filename: '{element}OtherData',"

##Dropdown2
if 'I' in element:
    plus_versEle = element.split('I')[0] + '+' * (len(element.split('I')) - 2)
    str2 = f'<a class="dropdown-item" href="{element}Other.html">{plus_versEle}</a>'
    rep2 = f'<a class="dropdown-item active" href="{element}Other.html">{plus_versEle}</a>'
else:
    str2 = f'<a class="dropdown-item" href="{element}Other.html">{element}</a>'
    rep2 = f'<a class="dropdown-item active" href="{element}Other.html">{element}</a>'
ind2 = format_hold_intro.find(str2)
#Key element case, it is already active so there is no inactive version
if ind2 < 0:
    rep2 = str1

##Header
if 'I' in key:
    el_name = plus_versKey.split('+')[0]
    pls_sym = plus_versKey.count('+') * '+'
    str3 = f'{el_name}<sup>{pls_sym}</sup> Other data'
else:
    str3 = f'{key} Other data'
if 'I' in element:
    el_replace = plus_versEle.split('+')[0]
    pls_replace = plus_versEle.count('+') * '+'
    rep3 = f'{el_replace}<sup>{pls_replace}</sup> Other data'
else:
    rep3 = f'{element} Other data'
ind3 = format_hold_intro.find(str3)
ind3

##title
if 'I' in key:
    str5 = f'<title>{plus_versKey}</title>'
else:
    str5 = f'<title>{key}</title>'
if 'I' in element:
    rep5 = f'<title>{plus_versEle}</title>'
else:
    rep5 = f'<title>{element}</title>'
    
##NIST URL
strRef = f'href="https://physics.nist.gov/cgi-bin/ASD/energy1.pl?de=0&spectrum={key_no_I}+{num_ion_key}&submit=Retrieve+Data&units=0&format=0&output=0&page_size=15&multiplet_ordered=0&conf_out=on&term_out=on&level_out=on&unc_out=1&j_out=on&lande_out=on&perc_out=on&biblio=on&temp=">'
url_ref = nist_urls[nist_urls.index == element]['URL'][0]
urlRef = 'href='+ '\"' + url_ref+'\">'
ind6 = format_hold_intro.find(strRef)

intro_format = format_hold_intro.replace(str1, rep1, 2)
#intro_format = intro_format.replace(stra, repa, 2)
intro_format = intro_format.replace(str2, rep2, 2)
intro_format = intro_format.replace(str3, rep3, 2)
#intro_format = intro_format.replace(str4, rep4, 2)
intro_format = intro_format.replace(str5, rep5, 2)
intro_format = intro_format.replace(strRef, urlRef, 2)

if type(metastable) == str: #if not metastable, then remove metastable button
    str_metbut = '<button class="button btn noprint " id="showTable3" value="Metastable state data"  onmouseout="this.innerHTML=\'Metastable state data\'" style=\'width:120pt; color: black;\'>Metastable state data </button>'
    rep_metbut = ''
    indmb = intro_format.find(str_metbut)
    intro_format = intro_format.replace(str_metbut, rep_metbut)
    
if type(metastable) != str: #if metastable, add bottom text listing states
    str_metnames = '<b></b>'
    rep_metnames = '<b>'
    for k in metastable_states:
        rep_metnames += k + ' '
    rep_metnames += '</b>'
    intro_format = intro_format.replace(str_metnames, rep_metnames)


# In[16]:


# tabl_excel = ap_presentable.to_html(index = False)
# tabl_life = tabl_life #lifetimes
# #tabl_excel = htmls[3] #excel_copy
# #tabl_main = htmls[0] #save_copy

# #table indexed from when tbody starts, ignoring initial headers
# #table1 is up to lifetime_table
# #+9 is number of characters in tbody, which we don't want to include
# form_table1 = intro_format + '\n' 

# #form_table1 += header_name

# #form_table1 += '\n' + button_lst

# #form_table1 += '\n' + format_hold_title

# form_table1 += '\n' + '\n' + tabl_life[tabl_life.find('<tbody>\n') + 9:]

# form_table1 += '\n' + '\n' + format_hold_excel
# form_table1 += '\n' + '\n' + tabl_excel[tabl_excel.find('<tbody>\n') + 9:]

# form_table1 += '\n' + '\n' + format_hold_main
# form_table1 += '\n' + '\n' + tabl_main[tabl_main.find('<tbody>\n') + 9:]

# form_table1 += format_hold_end
# form_tables = form_table1 


# In[17]:


#nuclear table data for element
s = nuc_sub.to_html(index = False)
num_tr = s.count('<tr>')
rows = ''
for i in range(num_tr):
    rows += '<tr>\n' + '\t'
    start = s.find('<tr>')
    end = start + s[start:].find('</tr>') + 7 #the tr blocks
    subset = s[start:end]
    num_td = subset.count('<td>')

#     subset = subset.replace('<td>NaN', '<td style = "display:none">NaN') #hide NaNs
#     subset = subset.replace('<td></td>', '<td style = "display:none"></td>') #hide empty rows
#     subset = subset.replace('<td>E', '<td style = "display:none">E') #hide Keys
    for j in range(num_td):
        
        result = re.search('<td>(.*)</td>', subset)
        row = '<td>' +result.group(1)+'</td>'
        q = subset.find(row)
        subset = subset[q + len(row):] #iterates through rows
        if j == 0:
            #superscript the isotope number
            row = '<td>' + '<sup>' + row.split(element_noI)[0].split('<td>')[1] + '</sup>' + element_noI + '</td>' 
        if j in [1, 2, 7, 8,10, 11, 13, 14]: #keys, theory numbers
            row = row.replace('<td>', '<td style = "display: none">')

#         elif j in [5, 6, 7, 8]: #references
#             inside = re.search('<td>(.*)</td>', row).group(1) #text inside <td>
#             if inside != '':
#                 if j == 5: #don't display the 1
#                     row = row.replace('<td>', '<td style = "display: none" class="nr3">')
#                 elif j == 6: #don't display the 1
#                     row = row.replace('<td>DOI:', '<td style = "display: none" class="nr4">')
#                 if j == 7: #don't display the 1
#                     row = row.replace('<td>', '<td style = "display: none" class="nr">')
#                 elif j == 8: #don't display the 1
#                     row = row.replace('<td>DOI:', '<td style = "display: none" class="nr2">')
        if j == (num_td - 1): #don't tab on last entry
            rows += row + '\n'
        else:
            rows += row + '\n' + '\t'
    rows += '</tr>\n'
        #print(row, i)
        
    #print(subset)
    s = s[end:]


# In[18]:


rows = rows.replace('&lt;sup&gt;', '<sup>')
rows = rows.replace('&lt;/sup&gt;', '</sup>')
rows = rows.replace('NaN', "")
rows_nuc = rows
# print('NUCLEAR')
# print(rows)


# In[19]:


#nuclear to subscript. Nuclear does not need to go to subscript, throws off another column
# sub_scripts = ['1/2', '3/2', '5/2', '7/2', '9/2', '11/2']
# htmls = [rows] 
# for i in sub_scripts:
#     for j, k in enumerate(htmls):
#         htmls[j] = htmls[j].replace('%s' % i, '<sub>%s</sub>' % i)
# nuc_tabl = htmls[0]
# print(nuc_tabl)


# In[20]:


#excel data, nuclear
# nuc_exl = nuc_sub.to_html(index = False)
# nuc_exl = nuc_exl[nuc_exl.find('<tbody>'):]
# nuc_exl = nuc_exl.replace("NaN", "")
# print(nuc_exl)


# In[21]:


plus_versEle = element.split('I')[0] + '+' * (len(element.split('I')) - 2)
hyper_fname = r'C:\Users\dmgame\Documents\SafronovaResearch\LifetimesWebsite\OtherData\%s_hyperfine.xlsx' % (plus_versEle)
hyper = pd.read_excel(hyper_fname, 
                    engine='openpyxl', header = 0,  usecols = [0,1, 2, 3, 4, 5])
hyper.dropna(how = 'all', inplace = True)


# In[22]:


col1 = hyper.columns[0] #column 1 name
if 'Unnamed' in hyper.columns[0]: #isotope not in header row
    #rename columns to isotope, and done
    hyper.rename(columns = {col1: "Isotope"}, inplace = True)
#     empty_row = pd.DataFrame([[np.nan] * len(hyper.columns)], columns=hyper.columns)
#     hyper = empty_row.append(hyper, ignore_index=True)
#     hyper.loc[0, 'Isotope'] = hyper['Isotope'][1] #put in isotope name
#     hyper.loc[1, 'Isotope'] = ''
#     hyper.loc[0, col1] = col1
#     hyper = hyper[1:] # drop first now NaN row
    
else: #need to put first isotope name in value row
    col1 = hyper.columns[0]
    #empty_row = pd.DataFrame([[np.nan] * len(hyper.columns)], columns=hyper.columns)
    #hyper = empty_row.append(hyper, ignore_index=True)
    hyper.loc[0, col1] = col1
    hyper.rename(columns = {col1: "Isotope"}, inplace = True)

hyper[0:3]


# In[23]:


#rename hyper, draw title
# hyper_ele = hyper['Unnamed: 0'][0]
# hyper.drop(columns = ['Unnamed: 0'], inplace = True)
# print(hyper_ele)

hyper = hyper.rename(columns = {"Ref.": "Key1", "Ref..1": "Key2"})
hyper.reset_index(inplace = True, drop = True)
hyper_html = hyper.to_html(index = False)


# In[24]:


#add in correct titles, doi and ref values
ref1s = []
ref2s = []
doi1s = []
doi2s = []
for i in range(len(hyper)):
    if 'E' in str(hyper['Key1'][i]):
        ref1s.append(ref_exl.loc[ref_exl['Ref'] == hyper['Key1'][i]]['Name'].values[0]) #the full reference
        doi1s.append(ref_exl.loc[ref_exl['Ref'] == hyper['Key1'][i]]['DOI'].values[0])
    else:
        ref1s.append('')
        doi1s.append('')
    if 'E' in str(hyper['Key2'][i]):
        
        if str(hyper['Key2'][i]).count('E') == 1: #1 reference
            ref2s.append(ref_exl.loc[ref_exl['Ref'] == hyper['Key2'][i]]['Name'].values[0])
            doi2s.append(ref_exl.loc[ref_exl['Ref'] == hyper['Key2'][i]]['DOI'].values[0])#the full reference
        else:
            #print(i, str(hyper['Key2'][i]), str(hyper['Key2'][i]).count('E'))
            r1 = hyper['Key2'][i].split(',')[0]
            r2 = hyper['Key2'][i].split(',')[1].strip(' ')
            ref2s.append((ref_exl.loc[ref_exl['Ref'] == r1]['Name'].values[0], ref_exl.loc[ref_exl['Ref'] == r2]['Name'].values[0]))
            doi2s.append((ref_exl.loc[ref_exl['Ref'] == r1]['DOI'].values[0], ref_exl.loc[ref_exl['Ref'] == r2]['DOI'].values[0]))
    else:
        ref2s.append('')
        doi2s.append('')
hyper['Ref1'] = ref1s
hyper['DOI1'] = doi1s
hyper['Ref2'] = ref2s
hyper['DOI2'] = doi2s
hyper[0:3]


# In[25]:


#get the hyperfine constant tabular data
s = hyper.to_html(index = False)
num_tr = s.count('<tr>')
rows = ''
for i in range(num_tr):
    rows += '<tr>\n' + '\t'
    start = s.find('<tr>')
    end = start + s[start:].find('</tr>') + 7 #the tr blocks
    subset = s[start:end]
    num_td = subset.count('<td>')

    for j in range(num_td):
        result = re.search('<td>(.*)</td>', subset) 
        row = '<td>' +result.group(1)+'</td>'
        q = subset.find(row)
        subset = subset[q + len(row):] #iterates through rows
        if j == 0:
            #superscript the isotope number
            if plus_versEle in row: #one of the isotope names
                if '+' in plus_versEle:
                    #print(plus_versEle)
                    row = '<td>' + '<sup>' + row.split(plus_versEle)[0].split('<td>')[1] + '</sup>' + plus_versEle.split('+')[0] + '<sup>' + '+' '</sup>' + '</td>'
                else:
                    row = '<td>' + '<sup>' + row.split(plus_versEle)[0].split('<td>')[1] + '</sup>' + plus_versEle + '</td>'
                #print(row)

        
        if 'E' in subset: #need to have ref button
            if j == 4: #row with the value
                #print(row)
                row = row.replace('</td>', ' <button type="button" class="btn btn-primary Ref1" data-toggle="modal" data-target="#exampleModalCenter">Ref</button></td>')
        if j in [3, 5]: #keys
            row = row.replace('<td>', '<td style = "display: none">')
            

            
        elif j in [6, 7, 8, 9]: #references
            inside = re.search('<td>(.*)</td>', row).group(1) #text inside <td>

            if j in [6, 8]: #the references
                if inside != '':
                    row = row.replace('<td>', '<td style = "display: none" class="nr">')
                else:
                    row = row.replace('<td></td>', '<td style = "display: none">')
                
            elif j in [7, 9]: #the doi's
                row = row.replace('<td>DOI:', '<td style = "display: none" class="nr2">') #if DOI
                row = row.replace('<td></td>', '<td style = "display: none">') #if no DOI
                
        if j == (num_td - 1): #don't tab on last entry
            rows += row + '\n'
        else:
            rows += row + '\n' + '\t'
    rows += '</tr>\n'
    s = s[end:] #next section
    
rows = rows.replace('NaN', '')


# In[26]:


#turn hfine into subscript
sub_scripts = ['1/2', '3/2', '5/2', '7/2', '9/2', '11/2']
htmls = [rows] #save_copy, Lifetimes, no_error, excel_copy
for i in sub_scripts:
    for j, k in enumerate(htmls):
        htmls[j] = htmls[j].replace('%s' % i, '<sub>%s</sub>' % i)
hfine_tabl = htmls[0]
# print("HYPER")
# print(hfine_tabl)


# In[27]:


# #excel table hyperfine constants
# hfine_exl = hyper.to_html(index = False)
# hfine_exl = hfine_exl[hfine_exl.find('<tbody>'):]
# hfine_exl = hfine_exl.replace("NaN", "")
# print(hfine_exl)


# In[28]:


meta_key_name = r"C:\Users\dmgame\Documents\SafronovaResearch\LifetimesWebsite\OtherData\Metastable_key.xlsx"
meta_key = pd.read_excel(meta_key_name, engine = "openpyxl", header = None, names = ['Ref', 'Name'])
meta_key.dropna(how = 'all', inplace = True)


# In[29]:


#set up key file with refs
doi_holder = []
name_holder = []
for i in range(len(meta_key)):
    try:
        doi_name = meta_key['Name'][i].split('DOI:')[1]
    except IndexError:
        doi_name = ''
    doi_holder.append(doi_name)
    name_str = meta_key['Name'][i].split('DOI')[0]
    last_comma = name_str.rfind(',')#finds last comma
    name_holder.append(name_str[:last_comma]) #removes last comma
meta_key['DOI'] = doi_holder
meta_key['Name'] = name_holder
meta_key


# In[30]:


if type(metastable) != str:
    split = metastable[metastable['Theory'] == 'Transition'].index[0]
    top_tbl = metastable[:split].copy()
    bot_tbl = metastable[split:].copy()

    top_tbl = top_tbl.rename(columns = {'Unnamed: 0': 'State'})
    top_tbl.dropna(axis = 1, how = 'all', inplace = True)
    top_tbl.dropna(axis = 0, how = 'all', inplace = True)
    try:
        for i in range(len(top_tbl)):
            if top_tbl['Expt. Ref.'][i] == top_tbl['Expt. Ref.'][i]: #string value, not a NaN
                #print(top_tbl['Expt. '][i] + top_tbl['Expt. Ref.'][i])
                top_tbl.loc[i,'Expt. '] = top_tbl['Expt. '][i] + ' ' + top_tbl['Expt. Ref.'][i]
            if top_tbl['Theory Ref.'][i] == top_tbl['Theory Ref.'][i]: #string value, not a NaN
                #print(top_tbl['Expt. '][i] + top_tbl['Expt. Ref.'][i])
                top_tbl.loc[i,'Theory'] = top_tbl['Theory'][i] + ' ' + top_tbl['Theory Ref.'][i]
        top_tbl.drop(axis = 1, columns = ['Theory Ref.', 'Expt. Ref.'], inplace = True)
    except KeyError: #RaII case, missing entire columns
        pass
    top_tbl
    


# In[31]:


if type(metastable) != str:
    for i in meta_key.Ref.values:
        print(i)


# In[32]:


if type(metastable) != str:
    #add on ref1, ref2
    #drop columns
    # go to html
    #replace in string: ref1 = 
    s = top_tbl.to_html(index = False)
    num_tr = s.count('<tr>')
    rows = ''
    for i in range(num_tr):
        rows += '<tr>\n' + '\t'
        start = s.find('<tr>')
        end = start + s[start:].find('</tr>') + 7 #the tr blocks
        subset = s[start:end]
        num_td = subset.count('<td>')
        #print(subset)

        for j in range(num_td):
            result = re.search('<td>(.*)</td>', subset) 
            row = '<td>' +result.group(1)+'</td>'
            q = subset.find(row)
            subset = subset[q + len(row):] #iterates through rows
            #print(row)
            for ref in meta_key.Ref.values: #ref1, ref2, ...
                if ref in row:
                    row = row.replace(ref, '<button type="button" class="btn btn-primary Ref1" data-toggle="modal" data-target="#exampleModalCenter"> Ref</button>')
                    row += '\n' +  '\t' + '<td style = "display:none" class="nr">' + meta_key[meta_key['Ref']== ref]['Name'].values[0] + '</td>'
                    row += '\n' + '\t' + '<td style = "display:none" class="nr2">' + meta_key[meta_key['Ref']== ref]['DOI'].values[0] + '</td>'
                    #print(row)

            #rows += row + '\n' + '\t'
            if j == (num_td - 1): #don't tab on last entry
                rows += row + '\n'
            else:
                rows += row + '\n' + '\t'
        rows += '</tr>\n'
        s = s[end:] #next section

    rows = rows.replace('NaN', '')


# In[33]:


print(rows)


# In[34]:


if type(metastable) != str:
    htmls = [rows] #
    for i in sub_scripts:
        for j, k in enumerate(htmls):
            htmls[j] = htmls[j].replace('%s' % i, '<sub>%s</sub>' % i)
    mettop_tabl = htmls[0]
#     print("Meta Top")
#     print(hfine_tabl)
    


# In[35]:


if type(metastable) != str: #metastable table 2
    #split index where second table starts
    split = metastable[metastable['Theory'] == 'Transition'].index[0]
    #top_tbl = metastable[:split].copy()
    bot_tbl = metastable[split:].copy()
    
#     top_tbl = top_tbl.rename(columns = {'Unnamed: 0': 'State'})
#     top_tbl.dropna(axis = 1, how = 'all', inplace = True)
#     top_tbl.dropna(axis = 0, how = 'all', inplace = True)
    
    bot_tbl.at[split, 'Unnamed: 0'] = 'Initial'
    bot_tbl.at[split, 'Property'] = 'Final'
    bot_tbl.dropna(axis = 1, how = 'all', inplace = True)
    
    
    for i in range(len(bot_tbl.columns)):
        #rename header into the correct titles from excel file
        bot_tbl = bot_tbl.rename(columns = {bot_tbl.columns[i] : bot_tbl[bot_tbl.columns[i]][split]}) 

    #drop now unneccesary row
    bot_tbl.drop(axis = 0, index = split, inplace = True)

    bot_tbl.dropna(axis = 0, how = 'all', inplace = True)
    bot_tbl.reset_index(inplace = True, drop = True)
    
    #top half metastable state
#     mtop_html = top_tbl.to_html(index = False)
#     mtop_html = mtop_html[mtop_html.find('<tbody>'):]
#     mtop_html = mtop_html.replace('NaN', '')
    
#     sub_scripts = ['1/2', '3/2', '5/2', '7/2', '9/2', '11/2']
#     htmls = [mtop_html] #save_copy, Lifetimes, no_error, excel_copy
#     for i in sub_scripts:
#         for j, k in enumerate(htmls):
#             htmls[j] = htmls[j].replace('%s' % i, '<sub>%s</sub>' % i)
#     mtop_html = htmls[0]
    #print(mtop_html)
    #print('--------')
    
    #bottom half metastable 
    mbot_html = bot_tbl.to_html(index = False)
    mbot_html = mbot_html[mbot_html.find('<tbody>'):]
    mbot_html = mbot_html.replace('NaN', '')
    
    sub_scripts = ['1/2', '3/2', '5/2', '7/2', '9/2', '11/2']
    htmls = [mbot_html] #save_copy, Lifetimes, no_error, excel_copy
    for i in sub_scripts:
        for j, k in enumerate(htmls):
            htmls[j] = htmls[j].replace('%s' % i, '<sub>%s</sub>' % i)
    mbot_html = htmls[0]
    metbot_tabl = mbot_html.replace('mB', '&mu;<sub>B</sub>')
#     print("Meta Bot")
#     print(mbot_html.replace('mB', '&mu;<sub>B</sub>'))
#     print(intro_format + '\n' + rows_nuc + '\n' + format_hold_hyp + '\n' + 
#           hfine_tabl + '\n' + format_hold_met1 + '\n' + mettop_tabl + '\n' + 
#           format_hold_met2 + metbot_tabl + '\n' + format_hold_end)


# In[36]:


if type(metastable) != str:
    if 'Expt. ' not in top_tbl.columns: #no experiment value,  load in different css
        print('no experiment values')
        with open(r"C:\Users\dmgame\Documents\SafronovaResearch\LifetimesWebsite\Format_csvs\OtherData\Hyperfine_to_metastableNoExp.txt", encoding="utf8") as file:
            format_hold_met1 = file.read()


# In[37]:


form_tables = intro_format + '\n' + rows_nuc + '\n' + format_hold_hyp + '\n' 
form_tables += hfine_tabl + '\n'
if type(metastable) != str:
    form_tables += format_hold_met1 + '\n' + mettop_tabl + '\n'
    form_tables += format_hold_met2 + metbot_tabl + '\n' 
form_tables += format_hold_end
#print(form_tables)


# In[38]:


fname = "ElementsHTMLs\%sOther.html" % (element)
fname


# In[39]:


text_file = open(fname, "wb")
text_file.write(form_tables.encode('utf8'))
text_file.close()

