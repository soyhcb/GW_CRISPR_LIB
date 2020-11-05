# Genome-wide CRISPR Lib
<img src="core/static/assets/imgs/SIAIS-Big-LOGO.png" style="height:50px">   

genome-wide CRISPPR Lib -new version

## Index
- [Genome-wide CRISPR Lib](#genome-wide-crispr-lib)
  - [Index](#index)
  - [Site Address](#site-address)
  - [Search Example](#search-example)
  - [Update Log 2020.09.15](#update-log-20200915)
    - [Import tsVector and GinIndex](#import-tsvector-and-ginindex)
    - [Use django-extensions and ipython for django shell](#use-django-extensions-and-ipython-for-django-shell)
    - [Query Process Improvement](#query-process-improvement)
    - [TODO](#todo)
  - [Open and Close](#open-and-close)
    - [check the site actually works](#check-the-site-actually-works)
    - [Run on uWSGI](#run-on-uwsgi)
      - [run with cmd line](#run-with-cmd-line)
    - [Run on uWSGI and Nginx](#run-on-uwsgi-and-nginx)
      - [Run uWSGI with `.ini` file:](#run-uwsgi-with-ini-file)
      - [Run Nginx with configure](#run-nginx-with-configure)
      - [Run uWSGI as an emperor](#run-uwsgi-as-an-emperor)
  - [import data from csv to Database](#import-data-from-csv-to-database)
  - [Support Data Table Libs](#support-data-table-libs)
  - [How to add a new library](#how-to-add-a-new-library)
    - [Step 1 Create a New App in Site](#step-1-create-a-new-app-in-site)
    - [Step 2 Implement the App](#step-2-implement-the-app)
    - [Step 3 Make the Lib Accessible](#step-3-make-the-lib-accessible)

## Site Address
only available through Shanghaitech Intranet on `10.15.21.153:8989` currently 

## Search Example
```
AAA,BBB,ALX1,CCDC85A,CDH9,CDH20,CLEC14A,CCDS47813.1,CCDS9942.1
```

## Update Log 2020.09.15
Greatly improve the query performance.
### Import tsVector and GinIndex
<a href="https://www.postgresql.org/docs/10/datatype-textsearch.html">tsVector</a> speeds up Full Text Retrieval and Indexing query fields also speeds up the query. (theoretically, tsvector will not speedup our query of crisprs, but this allows us to use GinIndex more easily)  
<a href="https://www.postgresql.org/docs/9.5/gin-intro.html">GinIndex</a> is Natively supported by postgreSQL which is currently unique and can greatly speeds up the Full Text Retrieval.  

### Use django-extensions and ipython for django shell

Install the `django_extensions` extension app. Thsi allows us to see raw sql querys in database and analyze the performance.  
It also allows us to use IPython for shell. so we can use shortcuts such as `timeit` to analyze the performance.(The performance are recorded in `Notes.md`)  

### Query Process Improvement

Based on the analysis, we found that the origin filtering of `hit or miss` using SQL is insanely slow.(up to 20seconds for 500 genes)  
we imporve the logic, converting the result to a set ehich significantly improve theperformance.
Based on the test, 5000 genes in search box can be handled easily on serverside.(Client side may need sometime to render the table in browser.)  

### TODO

Based on the analysis, `df.to_html` function takes most of the time of propcessing. Hopefully we can find a new way to conver the table to a html. Or simply leave the job as a async job using `Celery`, and leave a `ajax` request on client side.  

## Open and Close
run
```
python manage.py collectstatic
```
before run on uWSGI.  

### check the site actually works
make sure `DEBUG` in `/core/settings.py` is `False`  
then run:
```
python manage.py runserver 0.0.0.0:{port}
```
open `localhost:{port}` in browser to check the site.  
> if all static files(`css`, `js`, ...) files are missing, you should check the `static` path is properly setted.  
> Details see <a href="https://docs.djangoproject.com/en/3.0/howto/static-files/">Django Tutorial</a>  

The site actually works nows, but we prefer to deploy it with `uWSGI` and `Nginx`  
see <a href="https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html">Why Django + uWSGI + Nginx?</a>
<a href="https://www.cnblogs.com/suguangti/p/11334692.html">A recommended Chinese tutorial.</a>

### Run on uWSGI
if the site runs well with `runserver` command, you can deploy the site on `uWSGI`  
<a href="https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/uwsgi/">Django uWSGI tutorial</a>  

#### run with cmd line
Run on backgrund:
```
uwsgi --http :{port} --module core.wsgi --daemonize ./files/logs/uwsgilog.log --pidfile ./files/uwsgi.pid
```

Close uWSGI:
```
uwsgi --stop ./files/uwsgi.pid
```

Not run on backgrund:
```
uwsgi --http :<port> --module core.wsgi
```

### Run on uWSGI and Nginx
Both `uWSGI`'s and `Nginx`'s `config` ot `ini` files are already written.  
Details see <a href="https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html">Official Instrauction</a>
#### Run uWSGI with `.ini` file:

```
uwsgi --ini uwsgi.ini
```

#### Run Nginx with configure
Link current sites's config to Nginx global config:
```
ubuntu:
sudo ln -s ./lib_nginx.conf /etc/nginx/sites-enabled/

centos:
sudo ln -s ./lib_nginx.conf /etc/nginx/init.d/
```
check the `conf` with
```
sudo nginx -t
```
> if the test fails:
>> delete the syslink generated and copy the file to enabled site directly
```
sudo rm /etc/nginx/sites-enabled/lib_nginx.conf
sudo cp ./lib_nginx.conf /etc/nginx/sites-enabled/
```

> In CentOS7, Nginx weill not run other `.conf` file under `/etc/nginx/init.d/`  
>> modify `/etc/nginx/nginx.conf`  
>> include the `conf` file explicitly with in the `http` area.
Restart Nginx:
```
sudo /etc/init.d/nginx restart
# or
sudo service nginx restart
```
#### Run uWSGI as an emperor
Running uWSGI as an emperor allows uWSGI restarts web server as the config amended, allows multiple webservers in parallel.  
<a href="https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html">See Details (at the bottom)</a>  
```
uwsgi --emperor /etc/uwsgi/vassals --uid www-root --gid www-root –daemonize
```
It's not safe to run uWSGI as `root`, so specify `--uid` and `--gid` as another non-root user or number(e.g. 1000)
## import data from csv to Database

> postgreSQL is recommended

```
python ./manage.py shell < importCSV.py
```

## Support Data Table Libs

Details see <a href="https://datatables.net/download/index">DataTables</a>

> Buttons
>> HTML5 export (Excel, CSV, PDF...)

> JSZip
>> Required for  HTML5 export Excel

> pdfmake
>> Required for the PDF HTML5 export button.

> SearchPanes-1.1.1
>> Search panels for DataTables allowing rapid and customisable filtering.

> ColRecorder
>> Click-and-drag column reordering.

> RowRecorder
>> Click-and-drag row reordering.

> FixedHeader
>> Sticky header and / or footer for the table.

## How to add a new library

Considering we may have new libs in future, we can simply add the new lib to this site rather than create a new site. Here are the steps of creating a new lib.

> If you are familiar with Django, you can simply copy the whole `crispr_lib` app and modify the models, views, templates and so on to meet the requirement of the new lib.  
> Then register the app, import your data and bring it online.

### Step 1 Create a New App in Site
**Create the app**
```
python manage.py startapp {your app name}
```

### Step 2 Implement the App

**Create model**  
In `{your_app}/models.py`, create a new model. This should comply with your data. Be cautious in choosing Field types <a href="https://docs.djangoproject.com/en/3.0/ref/models/fields/">See Official Doc</a> It will be tricky to change field type once there are data in the database.
> just copy the model in `crispr_lib/models.py` and modify it.

**Create View**  
In `{your_app}/views.py`, import the model you just created and create a new view. This defines how the site respond to the request.  
Make sure the function takes `request` as a input. `request.method==POST` means user upload something to server(e.g. a report), usually it will be `GET`.  
> just copy the view in `crispr_lib/views.py` and modify it.

*How does the view return a table to the page?*  
*database --query--> queryset -> pandas.dataframe(pd.df) --process--> pd.df.to_html*  

**Create Template**
In `core/template/pages` create your template in corresponding directory (usually it will br dynamic.)  
> Recommended >> just copy the templates of `crispr_lib` and modify it.  
The basic structure should be remained.  

In `core/template/navigation.html` add new the lib to `#navbar-links` and set `id="you-lib-id"`.
In `<script>` area, find and modify or simply add:
```
var current = document.getElementsByClassName("active");
current[0].className = current[0].className.replace(" active", "");
var currpage = document.getElementById("you-lib-id")
currpage.className += " active";
```
This will set the active page on navbar to current page.  
In `core/template/pages/static/home.html`, add the link to the new lib.


**Admin View**  
In `{your_app}/admin.py` (create one if it doesn't exists). Create you admin view and register it to your model.  
`list_filter` defines the filter of instances in list view.  
`list_display` defines the fields shown in the field.  
`fieldsets` defines how the fields will be categoried and palced on the detail page.  
> just copy the view in `crispr_lib/admin.py` and modify it.  

### Step 3 Make the Lib Accessible

**Register the app to the site.**  
In `core/setting.py` find `INSTALLED_APPS`, and add your app into it.
> You shuold add the app earlier to run tests.

**Register a URL**  
In `{your_app}/your_app/`. create a new `urls.py`.
> just copy the view in `report/urls.py` and modify it.  

include the url of this app in `core/urls.py`

**Migrate the App and Bring it onlone.**  
In `report/models.py` find `class ReportCategory` under `class Report`:  
add `YOUR_LIB = {value in database}, _('name  for human to read')` where `{value in database}` should be a integer *Don't change the values of existed categories*. This allows users choosing the new lib as the report category.

To make the app in database
```
python manage.py makemigrations
python manage.py migrate
```

**Import Lib Data**  
Modify `importCSV.py` and import data to the database.
```
python manage.py shell < importCSV.py
```