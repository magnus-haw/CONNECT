import requests
import feedparser
from datetime import datetime
from bs4 import BeautifulSoup
from django_cron import CronJobBase, Schedule
from dateutil import parser as dateparser

from .models import JobPosting

class JobParser(object):

    def __init__(self, base="", query="", datefmt=""):
        self.url = base+query
        self.query = query
        self.base_url = base

    def parse(self):
        feed = feedparser.parse(self.url)
        return feed['entries']

    def add_to_db(self):
        ret = self.parse()

        for item in ret:
            #print(item["title"], item["link"], item["description"], dateparser.parse(item["published"]))
            try:
                jp, _ = JobPosting.objects.get_or_create(title=item["title"], link = item["link"], 
                                             description= item["description"], pubdate = dateparser.parse(item["published"]))
            except:
                pass

class AAS_Parser(JobParser):

    def __init__(self, base="https://jobregister.aas.org", query="/jobs/query?&body=plasma"):
        super().__init__(base=base, query=query)
      
    def parse(self):
        xhtml = requests.get(self.url)
        soup = BeautifulSoup(xhtml.content, 'lxml')
        rows = soup.find('table','tablesorter').find('tbody').find_all('tr')
        entries = [self.parse_row(row) for row in rows]
        return entries

    def parse_row(self,row):
        ret = {"title":None, "link":None, "org":None, 
                    "location":None, "published":None, 
                    "deadline":None, "status":None,}
        try:
            tds = row.find_all('td')
            ret["link"] = self.base_url + row.find('a')['href']
            ret["title"] = tds[0].string
            ret['org'] = tds[1].string
            ret["location"] = tds[2].string
            ret["published"] = tds[3].string
            ret["deadline"] = tds[4].string
            ret["status"] = tds[5].string
            ret["description"] = "%s, %s [posted %s, deadline %s]: %s "%(ret["location"], ret["org"], tds[3].string, tds[4].string, ret["status"])
        except:
            pass

        return ret


class APS_Parser(JobParser):

    def __init__(self, base="https://careers.aps.org", query="/jobs/?display=rss&keywords=plasma"):
        super().__init__(base=base, query=query)

class AGU_Parser(JobParser):

    def __init__(self, base="https://findajob.agu.org", query="/jobsrss/?keywords=plasma"):
        super().__init__(base=base, query=query)


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 480 # every 8 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'parser.my_cron_job'    # a unique code

    def do(self):
        aas, agu, aps = AAS_Parser(), AGU_Parser(), APS_Parser()
        return [p.add_to_db() for p in [aas,agu,aps]]

if __name__ == "__main__":

    #df = get_AAS_jobs()
    
    aas, agu, aps = AAS_Parser(), AGU_Parser(), APS_Parser()

    agu.add_to_db()
    aps.add_to_db()

    #base="https://jobregister.aas.org"
    #url = base + "/jobs/query?&body=plasma"
    #xhtml = url_get_contents(url).decode('utf-8')
    #soup = BeautifulSoup(xhtml, 'html.parser')
    #for link in soup.table.find_all('a'):
    #    print(base + link.get('href'))
    #df1= read_html("https://jobregister.aas.org/jobs/query?&body=plasma")[0]
    #print(df1.columns,df1)

# {% for entry in agujobfeed.entries %}
# 	    <tr><th scope="row"><a href="{{entry.link}}">{{entry.title}}</a></th></tr>
# 	    {% endfor %}
#             {% for entry in apsjobfeed.entries %}
# 	    <tr><th scope="row"><a href="{{entry.link}}">{{entry.title}}</a></th></tr>
#             {% endfor %}
# 	    {% for entry in aasjobfeed %}
#             <tr><th scope="row"><a href="{{entry.Link}}">{{entry.Title}}</a></th></tr>
#             {% endfor %}
# aasjobfeed = get_AAS_jobs()
# 
    