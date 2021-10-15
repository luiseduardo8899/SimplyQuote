# SimplyQuote
Simple quote, PO processing system in Django/Python. 

START WITH VIRTUAL ENV:
  #>pip3 install --user virtualenv
NOTE: virtualenv For Debian / Ubuntu:
  #>sudo apt install python3.8-venv

CREATE VIRTUAL ENV:
  #> python3 -m venv env


START VIRTUAL ENV:
  #> source env/bin/activate
  #> which python
  #> deactivate

------------------------------------
PACKAGES TO INSTALL:
  Django and file manipulation

  A. Execute 
    #> ./install_packages

  OR

  B. Install them one by one
      #> pip3 install django
      #> pip install xlwt			< create spreadsheets
      #> pip install xlrd			< read spreadsheets
      #> pip install pandas			< convert xls to html ( data analysis library )
      #> pip install xhtml2pdf		< convert html to PDF
      #> pip install django-crispy-forms    < convert Django models to forms

RECOMMENDED:
. Add Django extension to visual studio code
  https://marketplace.visualstudio.com/items?itemName=batisteo.vscode-django


------------------------------------
Summary to create virtual env and install required libraries:

#> git clone https://github.com/luiseduardo8899/SimplyQuote.git
#> cd SimplyQuote
#> python3 -m venv env
#> source env/bin/activate
#> ./install_packages

------------------------------------
LAUNCHING DJANGO SITE / APP

1.Make sure to run in virtual env
  #> source env/bin/activate;


2.Create migrations after model changes to update database
  #> cd QTR_site
  #>python3 manage.py makemigrations
  #>python3 manage.py migrate


3.Create superuser
  #> python3 manage.py createsuperuser


4.Run server:
  #> python3 manage.py  runserver


NOTE: If you need to reload database from scratch, remove migrations
To remove migrations:
  #> find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
  #> find . -path "*/migrations/*.pyc"  -delete
  #> rm -rf: db.sqlite3
  #> python manage.py makemigrations
  #> python manage.py migrate

