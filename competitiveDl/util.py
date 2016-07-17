import sys , os , re
from urllib2 import urlopen
from urllib import urlretrieve
from hashlib import md5
try:
    from bs4 import BeautifulSoup as bs
except :
    raise Exception("BeautifulSoup - 4 isn't downloaded \n pip install beautifulsoup4")
dynamic_dependencies =1

try:
    from selenium import webdriver
    from xvfbwrapper import Xvfb
except:
    dynamic_dependencies=0

import pdfkit

class Utilities(object):
    """ 
    Parent class that contains
    utility functions like
    get_pdf() , validate() ..etc

    """
    def __init__(self,site,html,dr,out='out.pdf'):
        self.page_as_string = html
        self.dr = dr
        self.out = out
        self.site = site

    def get_pdf(self):
        """
        Converts the existing page's html
        to PDF 

        """
        tmp_exists=0

        soup = bs(self.page_as_string)
        dir_name=''

        print "Generating PDF..."

        # Check if there are images
        if soup.find('img') is not None:
            tmp_exists=1
            imgs = soup.find_all('img')
            cwd = os.getcwd()
            dir_name = md5('competitive-dl').hexdigest() #Create a temporary folder
            done =0
            count=1
            
            # Fix folder name
            while done==0:
                if dir_name not in os.listdir('.'):
                    done=1
                else:
                    dir_name = md5('competitive-dl'+str(count)).hexdigest()
                    count=count+1
        
            os.mkdir(cwd+'/'+dir_name)
        
            count=1
            for img in imgs:

                file = dir_name+'/image'+str(count)+'.png'

                if img['src'][0] == '/':
                    img['src'] = 'http://'+self.site+'.com'+img['src']

                urlretrieve(img['src'],file) # Retrieve image
                img['src']=cwd+'/'+file
                del img['class']
                del img['style']
                del img['align']
                count = count+1

        curr_html = str(soup).decode('utf8')
        if self.dr[len(self.dr)-1]!='/':
            self.dr+='/'
        out_file = self.dr + self.out

        pdfkit.from_string(curr_html , out_file) # Convert to PDF !!

        print "Done ! Check out "+out_file+' !'

        # Remove temporary directory
        if tmp_exists:
            for k in os.listdir(dir_name):
                os.remove(dir_name+'/'+k)
            os.rmdir(dir_name)

    @staticmethod
    def validate_site(site,available,upcoming):
        """ 
        Method to check if 
        the given site is valid

        """

        if site not in available and site not in upcoming:
            print "Competitive-dl can\'t understand " + site
            sys.exit(0)
        elif site in upcoming:
            print "Downloading questions from"\
            " " + site + "will be available "\
            " soon ! Hang tight until the next"\
            " release !"
            sys.exit(0)

    @staticmethod
    def get_html(url):
        """
           function to get the static html source of a given url
           
        """
        page = urlopen(url).read()
        return page

    @staticmethod
    def get_dynamic_html(url):
        """
        Function to get dynamic html of given url

        """
        if not dynamic_dependencies:
            print "The extra depencies to scrape aren't"\
            " installed\n Please make sure you install them\n"\
            "(selenium , xvfbwrapper for python are the "\
            "extra dependencies)"
        else:
            source = ''
            virtual_display = Xvfb()
            virtual_display.start() # Start virtual display
            browser = webdriver.Firefox()
            print "Finding the given page...."
            browser.get(url)
            source = browser.page_source
            virtual_display.stop()

            return source 



class StaticScraper(Utilities):
    
    """
    A Scraper class to scrape from webpages where 
    content isn't injected dynamically using javascript
    
    """
    def __init__(self, site , contest , problem , dr='.' , out='out.pdf' , **others):
        
        self.site = str.lower(site)
        self.contest = contest
        self.problem = problem
        self.others = others
        self.url = ''
        self.page_as_soup = None
        self.page_as_string = ''
        self.problem_container = None
        self.problem_container_as_string = ''
        self.dr = dr 
        self.out = out
        self.available = ['spoj','codeforces'] # All sites that competitive-dl can scrape
        self.upcoming = ['topcoder'] # Sites for which scraping functionality isn't provided

        Utilities.validate_site(self.site , self.available , self.upcoming)

        self.scraper()


    @staticmethod
    def setTemplate(header,problem_container):
        """
        Returns a string with header
        and problem statement contained
        in the default html template

        """
        html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Problem</title>
                </head>
                <body>
                <div id="wrapper">
                    <h1 id="problem-head" style="width:50%;float:none;
                    margin:0 auto;text-align:center">
                        <span style="display:inline-block;">"""+header+"""</span>
                    </h1>
                    <div id="statement" style="width:60%;float:none;margin:0 auto;">
                        """+problem_container+"""
                    </div>
                </div>
                </body>
                </html>
                """
        return html

    def scraper(self):
        """
        scrapes from any given domain
    
        """
        def codeforces():
            """
            Scrapes problems from codeforces.com
                
            """
            
            # Building up the url
            url = "http://codeforces.com" # Start with the domain name
            url = url +'/'+'contest/'
            url = url + str(self.contest) +'/'

            if self.problem == 'all':
                url = url + 'problems'
            else:
                url = url + 'problem/'+str(self.problem)

            other_ops = self.others
            if 'language' in other_ops:
                if other_ops['language'] != 'en' and other_ops['language'] !='ru':
                    print("Invalid language \n"\
                        "en(English) and ru(Russian) "\
                        "are the only "\
                        "languages available")
                    sys.exit(0)
                else:
                    url = url + '?locale='+str(other_ops['language'])
            else:
                url = url + '?locale=en'

            self.url = url

            print "Pinging up codeforces...."

            # Get page source
            self.page_as_string = Utilities.get_html(url)
            soup = bs(self.page_as_string)
            self.page_as_soup = soup

            # Scrape contents
            
            header = soup.find('div',{'id':'header'}) # Fetches header
            header.extract()

            sidebar = soup.find('div',{'id':'sidebar'})# Fetches sidebar
            if sidebar is not None:
                sidebar.extract()

            head_menu = soup.find('div',{'class':'roundbox menu-box'}) # Fetches roundbox menu
            if head_menu is not None:
                head_menu.extract()

            second_level_menu = soup.find('div',{'class':'second-level-menu'})
            if second_level_menu is not None:
                second_level_menu.extract()

            lang_chooser = soup.find('div',{'class':'lang-chooser'})
            if lang_chooser is not None:
                lang_chooser.extract()

            footer = soup.find('div',{'id':'footer'})
            footer.extract()

            if soup.find('div',{'id':'pageContent'}) is not None:
                soup.find('div',{'id':'pageContent'})['style'] = ""\
                "margin:0 !important;"

            ulist = soup.find('div',{'class':'userListsFacebox'})
            if ulist is not None:
                ulist.extract()

            self.problem_container = soup.find('div',{'class':'problem-statement'})
            self.problem_container_as_string = str(self.problem_container)
            self.page_as_string = str(self.page_as_soup).decode('utf8')
            
        def spoj():
            """
            Scrapes problems from spoj.com
            (Uses default template)

            """
            url = "http://spoj.com" # Start with the domain name
            self.problem = str.upper(self.problem)
            url = url+"/problems/"+self.problem+'/'
            
            print "Pinging up spoj...."
            
            self.page_as_string = Utilities.get_html(url)
            soup = bs(self.page_as_string)
            
            p_header = soup.find('h2',{'id':'problem-name'})
            p_container = soup.find('div',{'id':'problem-body'})
            self.problem_container = p_container
            self.problem_container_as_string = str(p_container)
            
            self.page_as_string = StaticScraper.setTemplate\
            (str(p_header),self.problem_container_as_string)

            
            self.page_as_soup = bs(self.page_as_string)

        Utilities.validate_site(self.site , self.available , self.upcoming)
        #Above statement is added incase the user changes the site change the site

        eval(self.site + '()')

class DynamicScraper(Utilities):
    """
    Dynamic scraper class scrapes 
    webpages that have elements which
    are dynamically created using 
    javascript

    """
    def __init__(self,site,contest,problem,dr='.',out='out.pdf',**others):
        if not dynamic_dependencies:
            print "The extra depencies to scrape aren't"\
            " installed\n Please make sure you install them\n"\
            "(selenium , xvfbwrapper for python are the "\
            "extra dependencies)"
            sys.exit(0)

        else:
            self.site = str.lower(site)
            self.contest = contest
            self.problem = problem
            self.page_as_soup = None
            self.page_as_string = ''
            self.problem_container = None
            self.problem_container_as_string=''
            self.others = others
            self.dr = dr
            self.out = out
            self.available = ['codechef']
            self.upcoming = ['codejam']
            Utilities.validate_site(self.site , self.available , self.upcoming)
            self.scraper()

    def scraper(self):
        """
        Function to scrape from a 
        given competitive site

        """
        Utilities.validate_site(self.site , self.available , self.upcoming)

        def codechef():
            url = 'http://codechef.com'
            if self.contest!='practice' and self.contest!='':
                url = url+'/'+str(self.contest)
            url = url + '/problems/' + str(self.problem) + '/'

            print "Pinging up codechef...."

            self.page_as_string = Utilities.get_dynamic_html(url)

            print "Done !"

            soup = bs(self.page_as_string)
            self.page_as_soup = soup

            # Scrape contents
            
            maintable = soup.find('table',{'id':'maintable'})
            if maintable is not None:
                maintable.extract()

            header = soup.find('div',{'class':'header-container'})
            if header is not None:
                header.extract()

            header1 = soup.find('div',{'id':'header'})
            if header1 is not None:
                header1.extract()

            breadcrumbs = soup.find('div',{'id':'breadcrumbs'})
            if breadcrumbs is not None:
                breadcrumbs.extract()

            buttons_list = soup.find('ul',{'class':'button-list'})
            if buttons_list is not None:
                buttons_list.extract()

            todo = soup.find('div',{'class':'todo-widget'})
            if todo is not None:
                todo.extract()

            social = soup.find('div',{'class':'social-button-container'})
            if social is not None:
                social.extract()

            right = soup.find('div',{'id':'problem-right'})
            if right is not None:
                right.extract()

            submit = soup.find('ul',{'class':'bottom-bttn'})
            if submit is not None:
                submit.extract()

            comments = soup.find('div',{'id':'problem-comments'})
            if comments is not None:
                comments.extract()

            footer = soup.find('div',{'class':'footer-container'})
            if footer is not None:
                footer.extract()

            self.problem_container = soup.find('div',{'id':'problem-left'})
            self.problem_container_as_string = str(self.problem_container)
            self.page_as_soup = soup
            self.page_as_string = str(self.page_as_soup)

        Utilities.validate_site(self.site , self.available , self.upcoming) 
        #Above statement is added incase the user changes the site change the site 

        eval(self.site + '()')