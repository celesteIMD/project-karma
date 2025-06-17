RateMyRoom
Team Name: KARMA

Application description: RateMyRoom is a platform where users can submit feedback and comments regarding specific rooms available on Carleton University campus.

Screenshot of app:
<img width="1421" alt="image" src="https://github.com/user-attachments/assets/2de0e2c5-e288-40ce-8d12-e12a25a6b51a" />

1) Clone this with `git clone`
2) Open a terminal in the cloned folder
3) Install dependencies with `pip install -r requirements.txt` (on a lab computer, you can use `C:\Users\Public\ANACONDA\python.exe -m pip install requirements.txt`)
4) Create a file called `.env` in your cloned folder with the value `SECRET_KEY=SOMEVALUE` where `SOMEVALUE` is from this website: https://djecrety.ir/
5) Run `python manage.py makemigrations`
6) Run `python manage.py migrate`
6) Run management command with `python manage.py db_setup`. Make sure you have Google Chrome. Please wait patiently while the database is being set up.
Also note that this command will not work if there are already photos or reviews in the database.
6) To import data into the tags database:
   1) Open the `Database` tab on the right of the PyCharm interface and drag and drop the database file in this project (called `mydatabase`)
   2) Expand mydatabase until you see a list of tables, right-click on the table named `myRoom_tag` and select `Import Data from File(s)`
   3) Select the .cvs file found under `...\project-karma\static\csv\tags.csv`
   4) Press `OK` to import the data
7) Run the server with `python manage.py runserver`
8) See if it works at http://localhost:8000
