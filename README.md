# WebDesign
# TransitionManualInput 
is the main file, asks to enter element ("Fr", "CaII", etc.)
Creates 3 HTML files: Transition rate page, Matrix element page, Transition rate all states page

# OtherData 
is equivalent for Other data pages

# LoadFunctions.py 
reads in relevant functions

# Format_save_copy.py 
is for getting "all_state" data into pretty "save_copy", with necessasry columns and subscript.

# LoadInElement.py 
is what creates the pandas dataframe out of data

# To_HTML_CSV.py 
is for getting datatables into html files

# modsigfig.py 
is getting numbers into (##) format

# Process for creating the pages, TR, ME, All: 
Load TransitionManualInput on Jupyter notebook (or download it as a script)
and run all cells.
Enter the name of the element, i.e Cs or MgII. 
	This looks for the file with the name starting in that, so be careful of naming conventions.
	
	Files searched are datapol, database, rates1, and rates 2 in format "Data\%s\database%s.txt" where %s is the element name
	modify this in LoadInElement
	
	A pandas dataframe of the data (Transition rates, branching ratios, etc.) in correct error format will be created (save_copy)
	and turned into HTML.
	
	if you want to see the data before styling the variable is "all_state"
Make sure the HTML stylings are being read in from the correct location, starting with "with open('Format_csvs/TransitionRates/Intro_to_life_formatting.txt', 'r') as file:"

Transition rate HTML page is saved in format ""ElementsHTMLs\%sTranAuto.html" where %s is the element
	This same process with format read-ins in repeated for the Transition rate "all" page, and matrix element page
	
Other saved HTML's are "ElementsHTMLs\%sTranFull.html" and "ElementsHTMLs\%s.html" for "all" page and ME page respectively

# Process for creating the pages, Other:
Load OtherData on Jupyter notebook (or download it as a script)
and run all cells.

Enter name of the element, i.e Fr or CaII

Make sure file location pointers are correct

HTML page is saved as "ElementsHTMLs\%sOther.html" where %s is the name of the element

If you want to run all elements for TR, ME, All, Other generation run Master1
	Currently runs 12 elements, can be expanded by adding elements to top list
	
	Note: make sure that if you modify a notebook to run a specific element (like by saying element = "Be") 
	
	you comment this out in the version Master1 is running, or it will run the same element over and over again.
	
	You can tell this is happening based on Master1's print returns.





