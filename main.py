import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'Patreon'
HOMEPAGE = 'https://www.udemy.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME,HOMEPAGE,DOMAIN_NAME)


#Create Worker threads
def create_spiders():

    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True   #DIE WHENN MAINN EXITS
        t.start()



#Do next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread.name(),url)
        queue.task_done()





#Each queued link is a new job
def create_jobs():
    for link in file_to_set(queue):
        queue.put(link)
    queue.join()
    crawl()







#Check if there are items in queue and crawl them if needed
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links)>0:
        print(str(len(queued_links))+ ' links in queue')
        create_jobs()


create_spiders()
crawl()



