# Amazon Product Listing

## How to set up and run the project locally (including Celery and broker setup).
Ensure venv is activated. 
- Navigate to Django root project directory in Windows Powershell
- Activate venv with .venv/Scripts/activate
- Install celery with `pip install celery`
- Install results with `pip install django-celery-results`
- Install sqlalchemy with `pip install sqlachemy`
+ Ensure node.js is installed, node.js version used here is v
+ Install TailwindCSS, run the following in your terminal
  + `npm install -D tailwindcss`
  + `npx tailwindcss init`
+ Install DasiyUI
  + `npm i -D daisyui@latest`

## Instructions for scheduling and managing the periodic tasks.
- Ensure to create a new superuser account with `python manage.py createsuperuser`
- Go to admin panel for your Django website:
  - Run `python manage.py runserver` in terminal
  - Navigate to link _**localhost**/admin_ on your browser (note that your **_localhost_** will display in terminal)
  - Create new brands in Brands like Nike, Microsoft etc
  - 
  - For manual scrape operations, use the actions navbar at the top of Admin Brands page to scrape products of specific brands.

## How the web scraping is implemented, including any anti-scraping measures.
- The scraper goes to amazon.com and gets url for product of a specific brand, taking into consideration pagination.
  - To mitigate risks of getting blocked by amazon.com, several usable User-Agents are sourced for online and saved to be used in the scraping process.
- Information like name, asin, page are gotten from product url
- To get high-quality image url for each product
  - The scraper access each product page for products of a brand and gets the image url
- 

## Any assumptions or design decisions.

### Admin Panel
- Username: admin
- Email: admin@mail.com
- Password: admin
