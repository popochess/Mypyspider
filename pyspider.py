#!/usr/bin/env python
'''

parma1  => link
parma2  => depth

'''
import re
import sys
import urllib2
import urlparse
from traceback import format_exc
from Queue import Queue, Empty as QueEmpty

from BeautifulSoup import BeautifulSoup




class pyspider(object):

    def __init__(self, root, depth, locked=True):
        self.root = root
        self.depth = int(depth)
        self.locked = locked
        self.host = urlparse.urlparse(root)[1]
        self.urls = []
        self.links = 0
        self.followed_depth = 0
        self.URLdepth = 1
        self.followedURLs = []
        self.follow_num = 0
        self.ignorefile = ".avi|.jpg|.JPG|.doc|.ai|.avi|.mpg|.flv|.pdf|.xls|.ppt|.docx|.png"
        self.tree_arr = {}

    def run(self):
        
        #first run
        self.followedURLs = []
        self.followedURLs.append(self.root)
        self.follow_num = self.follow_num + 1

        page = Fetch(self.root)
        page.get_pageURLs()
        

        
        que_URLs = Queue() 
        que_depth = Queue()
        
         
        for url in page:
                        
            host = urlparse.urlparse(url)[1]
            if re.match(".*%s" % self.host, host) :
                que_URLs.put(url)
                que_depth.put(self.URLdepth)            
                if unicode("0:")+self.root not in self.tree_arr: #set up the first node of the tree 
                    self.tree_arr[unicode("0:")+self.root] = [unicode("1:")+url]
                else:
                    self.tree_arr[unicode("0:")+self.root].append(unicode("1:")+url)

        #print self.tree_arr 

        #print followedURLs 
        while que_URLs.empty() == False:
            try:
                url_q = que_URLs.get_nowait()

                d = que_depth.get()
                    
                
                if url_q not in self.followedURLs : 
                    try:
                        print "ready to fetch =>"+str(d)+":"+url_q+"*****"
                        #print str(d)+":"+url_q+"*****"
                        #print "fetch a link!"
                        
                        if d<self.depth and re.search(self.ignorefile,url_q) == None:
                            page = Fetch(url_q)    
                            self.follow_num = self.follow_num + 1
                            page.get_pageURLs()
                            for i,url_e in enumerate(page):
                                host = urlparse.urlparse(url_e)[1]
                                if url_e not in self.followedURLs and re.match(".*%s" % self.host, host): 
                                    #print "queue put()!!!!!=>>>>>>>>>>>>>>>>>>"+url_e
                                    que_URLs.put(url_e)
                                    print "  Queue => "+url_e
                                    que_depth.put(d+1)

                                    if unicode(d)+":"+url_q not in self.tree_arr:
                                        
                                        #print "I come in first time"
                                        #print "url_q=>"+url_q
                                        #print "url_e=>"+url_e
                                        url_d_l = unicode(d+1)+":"+url_e
                                        #print d_q

                                        #print  type(d_q)
                                        self.tree_arr[unicode(d)+":"+url_q] = [url_d_l]
                                    else:
                                        url_d_l = unicode(d+1)+":"+url_e
                                        
                                        #print "I come in again"
                                        #print "url_q=>"+url_q
                                        #print "url_e=>"+url_e
                                        self.tree_arr[unicode(d)+":"+url_q].append(url_d_l)

                        self.followedURLs.append(url_q)
                        #print "append!!!=>>>>>>>>>>>>>>>>>>>>>"+url
                                                 
                    except Exception, e:
                       print "ERROR! %s" % e+"url_q"
                       print format_exc()
                        
            except QueEmpty:
                break
        #print self.tree_arr
        print "finish!!"
        print "\n"*5
        print "print the tree map!!!\n\n"
        self.print_tree()
        print "total fetched URL numbers =>"+str(self.follow_num)

    def print_tree(self):

        stack = Stack(["0:"+self.root])    
        print "0:"+self.root
        last_d = ""
        while stack.hasdata():
            temp = stack.pop()    
             
            
            d = temp.split(":")[0]
            for i in range(int(d)):
               if i >0: 
                  print " ",
                  print " ",
               
               if i == int(d)-1 and last_d == d:
                   print "|--",
                   print temp,
                   print ""
               if i == int(d)-1 and last_d != d:
                   print "|--",
                   print temp,
                   print ""
            if self.tree_arr.has_key(temp):
                for u  in  (self.tree_arr[temp])[::-1]:
                    stack.push(u)

            
            last_d = d 
             

        
class Stack:
    def __init__(self, data):
        self._data = list(data)
    def push(self, item):
        self._data.append(item)
    def pop(self):
        item = self._data[-1]
        del self._data[-1]
        return item
    def toString(self):
        print self._data

    def hasdata(self):
        if  len(self._data)!= 0:
            return True
        else:
            return False

class Fetch(object):
    def __init__(self, url):
        self.url = url
        self.urls = []
        self.host = urlparse.urlparse(url)[1]

    def __getitem__(self, x):
        pass
        return self.urls[x]
    '''def _addHeaders(self, request):
        request.add_header("User-Agent", AGENT)
        print "agent =>"+AGENT
    '''
    def set_handle(self):
        try:
            handle = urllib2.build_opener()
        except IOError:
            return None
        return handle

    def set_request(self):
        url = self.url 
        try:
            request = urllib2.Request(url)
        except IOError:
            return None
        return request

    def get_pageURLs(self):
       
        #print "Fetch => "+self.url
            
        request = self.set_request()
        #print "request_g=>"+str(request)

        #self._addHeaders(request)

        handle = self.set_handle()
        #print "handle_g=>"+str(handle)

        if handle:
            try:
                content = unicode(handle.open(request).read(), "utf-8", errors="replace")
                self.html_parser(content)
                soup = BeautifulSoup(content)
                tags = soup('a')
            except urllib2.HTTPError, error:
                if error.code == 404:
                    print >> sys.stderr, "ERROR: %s -> %s" % (error, error.url)+"   urllib2.HTTPError"
                else:
                    
                    print >> sys.stderr, "ERROR: %s -> " % error +self.url 
                tags = []
            except urllib2.URLError, error:
                print >> sys.stderr, "ERROR: %s" % error
                tags = []
           
            for tag in tags:
               href = tag.get("href")  
               if href is not None:
                   url = self.url_join(self.url, href)
                   if url is not self.url and url != None:
                       self.urls.append(url)
    def html_parser(self,page):       
        #print page
        pass
        
                    
    def url_join(self,url, href):
        
        joined_url = urlparse.urljoin(url, href)
        if len(joined_url.split("http://"))>2:  #no outside link
            joined_url = None
         

        return joined_url 
        
if __name__ == '__main__':
    
    test = pyspider(sys.argv[1],sys.argv[2])
    test.run()  

