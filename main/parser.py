import urllib.request
from pandas import read_html, DataFrame
from bs4 import BeautifulSoup

def url_get_contents(url):
    """ Opens a website and read its binary contents (HTTP Response Body) """
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()

class objectview(object):
    def __init__(self, d):
        self.__dict__ = d

def get_AAS_jobs(base="https://jobregister.aas.org",query="/jobs/query?&body=plasma"):
    xhtml = url_get_contents(base+query).decode('utf-8')
    soup = BeautifulSoup(xhtml, 'html.parser')
    links =[]
    df= read_html(base+query)[0]
    for link in soup.table.find_all('a'):
        links.append(base + link.get('href'))
    df['Link'] = links
    listd = df.to_dict('records')

    return [objectview(d) for d in listd]

if __name__ == "__main__":

    df = get_AAS_jobs()
    print(df)

    #base="https://jobregister.aas.org"
    #url = base + "/jobs/query?&body=plasma"
    #xhtml = url_get_contents(url).decode('utf-8')
    #soup = BeautifulSoup(xhtml, 'html.parser')
    #for link in soup.table.find_all('a'):
    #    print(base + link.get('href'))
    #df1= read_html("https://jobregister.aas.org/jobs/query?&body=plasma")[0]
    #print(df1.columns,df1)
