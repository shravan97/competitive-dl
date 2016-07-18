Competitive - dl  :file_folder:
---------------- 

**Note :** This tool is to be used for **educational** pursoses **only** and not for any other commercial use

Features 
~~~~~~~~ 
- Download any problem/problem set from any contest/archives from any competitive website as PDF for offline practice !
	* You can download to any desired directory of your choice !
- Get the HTML source of the problem page as well as the problem container
- Get the problem statement , input & output samples as text  
- Competitive sites from which download is possible (so far):
	* `Codeforces <http://codeforces.com>`__  
	* `Spoj <http://spoj.com>`__
	* `Codechef <http://codechef.com>`__  

Demo 
~~~~ 
As a command line application (CLI) 
''''''''''''''''''''''''''''''''''' 
.. image:: https://cloud.githubusercontent.com/assets/10980285/16903220/75f5e1d4-4c95-11e6-87b4-92a1b49605a5.gif


As a module 
''''''''''' 
.. image:: https://cloud.githubusercontent.com/assets/10980285/16902720/b3dcdcb6-4c84-11e6-836f-f5af79642763.gif  

For sites with dynamic content like codechef , **StaticScraper()** is replaced with **DynamicScraper()**  


Requirements 
~~~~~~~~~~~~ 
General requirements 
'''''''''''''''''''' 
- Modules that get automatically installed
	- `pdfkit <https://pypi.python.org/pypi/pdfkit>`__
	- `BeautifulSoup4 <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`__
- Modules that'll have to be installed **manually**
	- `wkhtmltopdf <http://wkhtmltopdf.org>`__
		- ``sudo apt-get install wkhtmltopdf``  

Additional requirements (to scrape from dynamic sites) 
'''''''''''''''''''''''''''''''''''''''''''''''''''''' 
- Modules that get automatically installed
	- `selenium python <http://selenium-python.readthedocs.io/installation.html>`__
	- `python xvfbwrapper <https://pypi.python.org/pypi/xvfbwrapper/0.2.8>`__
- Modules that'll have to be installed **manually**
	- Xvfb (actually a requirement of xvfbwrapper)
		- ``sudo apt-get install Xvfb``

Installation 
~~~~~~~~~~~~ 
From this repository 
'''''''''''''''''''' 
.. code:: sh
	
	   git clone http://github.com/shravan97/competitive-dl 


.. code:: sh

	cd competitive-dl 


.. code:: sh

	python setup.py install  

Using pip 
''''''''' 
Coming up very soon !  


Usage 
~~~~~ 
As a CLI 
'''''''' 
.. code:: sh

	usage: competitive-dl [-h] [-s SITE] [-c CONTEST] [-p PROBLEM] [-d DIR] [-o FILENAME]
	               [-l LANGUAGE]
	
	optional arguments:
	  -h, --help   show this help message and exit
	  -s SITE      The competitive site , for eg. codeforces , spoj ...etc
	  -c CONTEST   Contest-id or archive , for eg. 682 , classical..etc
	  -p PROBLEM   Problem code , for eg. COINS , A , 1...etc
	  -d DIR       Directory where your file has to be saved
	  -o FILENAME  PDF file name
	  -l LANGUAGE  Language in which content has to be saved . This depends on the
	               languages offered by the competitive site

As a Module 
''''''''''' 

.. code:: python

	from competitiveDl import util
	c = util.StaticScraper('spoj','classical','PALIN',dr='/home/shravan97/Desktop/',out='favourite.gif')
	c.get_pdf()

Sample usage 
~~~~~~~~~~~~ 

.. code:: sh

	competitive-dl -s codeforces -c 682 -p C -o tree_problem.pdf 


.. code:: sh

	competitive-dl -s spoj -p PALIN -dir /home/shravan97/Desktop -o my_fav_problem.pdf 

  
Please check out the demo PDF files `here <http://github.com/shravan97/competitive-dl/tree/master/demo>`__


Listed below are a few cool upcoming features !

Upcoming 
~~~~~~~~ 
- Download problems with your own HTML template for the PDF !
- Merge multiple problems from different websites into a PDF with your own template !
- Download from a lot more competitive sites like `Topcoder <http://topcoder.com>`__ , 
`Hackerearth <http://hackerearth.com>`__ ....etc !  

Contributions 
~~~~~~~~~~~~~ 
If you find an idea that could be implemented here , please feel free to give a pull request or put that up as an issue `here <http://github.com/shravan97/competitive-dl/issues>`__ :smile:

Contributors 
~~~~~~~~~~~~ 
- `shravan97 <http://github.com/shravan97>`__

License 
~~~~~~~ 
The MIT License (MIT)
Copyright (c) 2016 SHRAVAN MURALI

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

**THIS SOFTWARE CAN BE USED FOR EDUCATIONAL PURPOSES ONLY**  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
