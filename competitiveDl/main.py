from util import Utilities as Ut , StaticScraper as Ssc , DynamicScraper as Dsc
from argparse import ArgumentParser as Ap
import sys

def get_options():
    parser = Ap()
    
    parser.add_argument('-s',
    dest="site",
    help="The competitive"\
    " site , for eg. "
    "codeforces , spoj ...etc")
    parser.add_argument('-c',
    dest='contest',
    help='Contest-id or archive , for '\
    'eg. 682 , classical..etc ')
    parser.add_argument('-p',
    dest="problem",
    help='Problem code ,'\
    ' for eg. COINS , A , 1...etc')
    parser.add_argument('-d',
    dest="dir",
    help="Directory where"\
    " your file has to be"\
    " saved")
    parser.add_argument('-o',
    dest="filename",
    help="PDF file name")
    parser.add_argument('-l',
    dest="language",
    help="Language in which "\
    "content has to be saved . "\
    "This depends on the languages"\
    " offered by the competitive site")

    args = parser.parse_args()

    values = {}
    if args.site is None:
        print "Please specify"\
        " the competitive website\n"\
        "For eg. codeforces , codechef...etc"
        sys.exit(0)
    else:
        values['site'] = args.site
        if args.contest is None:
            values['contest'] = ''
        else:
            values['contest'] = args.contest
        if args.problem is not None:
            values['problem'] = args.problem
        else:
            if args.site != 'codeforces':
                print "Competitive-dl "\
                "doesn't yet support "\
                "problem set downloads "\
                "from contests of sites "\
                "other than codeforces"
                sys.exit(0)
            else:
                values['problem']='all'
        if args.dir is not None:
            values['dr'] = args.dir
        if args.filename is not None:
            values['out'] = args.filename
        if args.language is not None:
            values['lang'] = 'en'

        return values

def mains():
    args = get_options()
    static_sites = ['codeforces',
                    'spoj',
                    'topcoder']
    dynamic_sites = ['codechef',
                     'codejam']
    scraper_obj = None
    if args['site'] in static_sites:
        scraper_obj = Ssc(**args)
    else:
        scraper_obj = Dsc(**args)

    scraper_obj.get_pdf()

if __name__=="__main__":
    mains()