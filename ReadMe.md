# Amazon Product Listing

## How to set up and run the project locally (including Celery and broker setup).
Ensure venv is activated
- Navigate to Django root project directory in Windows Powershell
- Activate venv with .venv/Scripts/activate
- Install Django withy `pip install Django`
- Install celery with `pip install celery`
- Install results with `pip install django-celery-results`
- Install results with `pip install django-celery-beat`
- Install sqlalchemy with `pip install sqlachemy`
- Install broker with `pip install redis`
- After all installations, apply necessary migrations for Django project with `python manage.py migrate`

To view products of a brand with minimal yet beautiful frontend, setup your system as follows:
+ Ensure node.js is installed, node.js version used here is v
+ Install TailwindCSS, run the following in your terminal
  + `npm install -D tailwindcss`
  + `npx tailwindcss init`
+ Install DasiyUI
  + `npm i -D daisyui@latest`

## Instructions for scheduling and managing the periodic tasks.
- Ensure to create a new superuser account with `python manage.py createsuperuser`
- How to go to admin panel for your Django website:
  - Run `python manage.py runserver` in terminal
  - Navigate to link _**localhost**/admin_ on your browser (note that your **_localhost_** will display in terminal)
  - Create new brands in Brands like Nike, Microsoft etc
  - For manual scrape operations, use the actions navbar at the top of Admin Brands page to scrape products of specific brands.
- To utilize scheduling and periodic tasking:
  - First start your broker. The redis application which is the broker used for this project has been made available already, simply run it this way:
    - Navigate to the root directory in your terminal
    - Run the command `./Redis-x64-3.0.504/redis-server`
  - Start the celery worker:
    - Open another terminal or Windows PowerShell with venv activated (see how to activate venv in the **How to set up and run the project locally** section of this documentation)
    - Ensure you are in the root directory 'amazonProductListing' and Start celery with command `celery -A amazonProductListing worker -l info`
    - Note that you might run into errors using celery with the above command on Windows due to multiprocessing limits. If this is the case, run celery instead as solo with command `celery -A amazonProductLisiting worker -l info -P solo`
  - Now you need to start celery beat, celery beat sends due tasks to the worker, to start beat:
    - Open another terminal or Windows PowerShell with venv activated
    - Ensure you are in the root directory 'amazonProductListing' and run command `celery -A beat -l info`
    - The beat has been set to run every 6-hours (check _settings.py_ file to adjust this behaviour if desired)

## How the web scraping is implemented, including any anti-scraping measures.
- Firstly, the scraper visits amazon.com and gets the url of products of specific brands defined in the admin panel, taking into consideration pagination.
  - To mitigate risks of getting blocked by amazon.com, several usable User-Agents are sourced for online and saved to be used in the scraping process.
- Information like name, asin, page are gotten from each product url
- To get high-quality image url for each product, the scraper accesses each product page for products of a brand and gets the image url
- Information of the saved product is saved to the database

## Any assumptions or design decisions.
- A large number of products do not have readily available sku, scraping for this info was jettisoned
- It is assumed that this Django project will be run in a Windows environment. However, for Linux most of the steps are similar except changes to commands like the use of `sudo`. The celery documentation is helpful instructions to run Linux environments.

## How To Run Code and View Frontend
To run the Django website:
- Run command `npm run dev` in a terminal with (venv activated) to utilize _**daisyUI**_
- Run `python manage.py runserver` in another terminal with venv activated to start the development server
- Navigate to link _**localhost**_ on your browser (note that your **_localhost_** will display in terminal):
  - A sample _localhost_ link(which will direct to the homepage) looks like this _http://127.0.0.1/8000_
- _localhost_/products will direct you to the products page
- The search bar can also be used to search for products of brands already saved in the database.
'
### Admin Panel
You can use the credentials below to create a easy-to-remember Superuser
- Username: admin
- Email: admin@mail.com
- Password: admin
