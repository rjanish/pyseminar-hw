bib_page.py

This script runs a bibtex database webapp on localhost.

To use, run the script:
	$ python bib_page.py
from a directory containing the 'templates' subdirectory, which must contain the template files 'base.html' and 'index.html'.  This script requires that the following packages must be installed: flask, flask-sqlalchemy, and pybtex

The file homework_10_refs.bib provides a test bibtex entry.  The webpage will allow you to upload any number of bibtex files, provide each one with a 'collection' name, and search the uploaded references.  Search by entering a comma seperated list of search terms in any of the reference attribute boxes, and the app will diplays the bibtex reference keys of any references matching those search terms (in the sql "LIKE" sense).  If nothing is entered in a box, it is condidered to match everything.  For example, clicking 'search' with each box empty dispays all references in the database, and searching with '1998, 1999, 2000' in the 'years' dialog and 'globular cluster' in the 'titles' dialog will display all references with 'globular cluster' in the title published in 1998, 1999, or 2000. 