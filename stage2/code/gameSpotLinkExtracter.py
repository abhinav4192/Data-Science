from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
from threading import Thread
import re
import urllib.request


# Get links for review pages of games.
def allReviewLinkExtractor():
    quote_page = 'https://www.gamespot.com/reviews/?page='
    f = open('gamelist.txt', 'w+', 100)
    for i in range(1, 693):
        try:
            f.write("Page number: " + str(i) + "\n")
            print("crawling page: {}".format(i))
            qp = quote_page + str(i)
            page = urlopen(qp)
            soup = BeautifulSoup(page, "lxml")
            for link in soup.find_all('a'):
                hr = link.get('href')
                if hr is None:
                    continue
                if "https" in hr:
                    continue
                if "reviews" in hr and hr.count('/') == 4:
                    f.write(hr + "\n")
                    f.flush()
        except:
            print("*********************** Failed  for page number:" + str(i) + "\n")
            time.sleep(15)


# get unique links for review pages
def uniqueReviewLinkExtractor():

    f = open("gamelist.txt")
    lines = list(set(f.readlines()))
    f.close()

    f = open("gameSpot_gamelist_unique.txt", 'w+')
    f.write("".join(lines))
    f.close()


# Threaded Gamelink extraction from review pages
def gameLinkExtractorThread(threadName, links, start, end):
    print("Start thread:" + threadName, start, end)
    regex = re.compile("sameAs\":\"(\S*)\"")
    quote_page = 'https://www.gamespot.com'
    f = open("gamelinks" + threadName + ".txt", 'w+', 1)
    for i in range(start, end):
        print(threadName + ":" + str(i))
        l = links[i]
        try:
            qp = quote_page + l
            page = urlopen(qp)
            page = str(page.read())
            searchObj = re.search(regex, str(page))
            if searchObj != None and len(searchObj.groups()) > 0:
                f.write(searchObj.group(1) + "\n")
                f.flush()
            else:
                print("Nothing found")
        except:
            print("*********************** Failed  for line number:" + str(i) + "\n")
            time.sleep(15)
    f.close()

# Gamelink extraction from review pages


def gameLinkExtractor():
    f = open("gameSpot_gamelist_unique.txt")
    lines = list(set(f.readlines()))
    f.close()
    threads = []
    for i in range(0, 30):
        threads.append(Thread(target=gameLinkExtractorThread, args=(
            "Thread_" + str(i), lines, i * 500, min((i + 1) * 500, len(lines)))))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# Gamelink extraction from review pages for failed pages
def failedLinkExtractor():
    fl = [9507, 2007, 7007, 7, 11507, 3007, 1006, 7506, 12506, 14506, 4506, 5006, 8507, 12007, 2507, 9007, 6007, 8197, 6193, 10278, 5278, 8776, 11778, 10783, 5781, 2778, 789, 11285,
          12279, 4777, 13824, 3379, 4388, 14381, 5881, 9876, 3884, 13389, 2876, 4874, 1890, 7379, 8874, 889, 5375, 998, 8982, 5482, 8450, 9487, 7487, 1493, 4496, 494, 5992, 6448, 12489]
    f = open("gameSpot_gamelist_unique.txt")
    lines = list(f.readlines())
    lines2 = [lines[i] for i in fl]
    f.close()
    threads = []
    for i in range(30, 31):
        threads.append(Thread(target=gameLinkExtractorThread, args=(
            "Thread_" + str(i), lines2, 0, len(lines2))))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# Gamelink combiner - combines results of threaded files in a single file.
def gameSpotLinkCombiner():
    linklist = []
    for i in range(0, 31):
        name = "gamelinks" + "Thread_" + str(i) + ".txt"
        f = open(name)
        for l in f.readlines():
            linklist.append(l)
        f.close()
    print(len(linklist), len(set(linklist)))
    linklist = sorted(list(set(linklist)))
    f = open("gameSpot_links_unique.txt", 'w+')
    f.write("".join(linklist))
    f.close()


# threaded method to download html pages from gamelinks
def downLoadHtmlPageThread(lines, start, end):
    for i in range(start, end):
        print("trying for number:", i)
        l = lines[i]
        try:
            file_name = "../gameSpot_HTML/" + l.split('/')[-2] + ".html"
            urllib.request.urlretrieve(l, file_name)
        except:
            print("Failed for number:", i)
            time.sleep(15)


# method to download html pages from gamelinks
def downLoadHtmlPage():
    f = open("gameSpot_links_unique.txt")
    lines = f.readlines()
    f.close()
    threads = []
    for i in range(0, 41):
        # print(i * 250, min((i + 1) * 250, len(lines)))
        threads.append(Thread(target=downLoadHtmlPageThread, args=(
            lines, i * 250, min((i + 1) * 250, len(lines)))))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# method to download failed html pages from gamelinks
def downLoadFailedHtmlPage():
    f = open("gameSpot_links_unique.txt")
    lines = f.readlines()
    f.close()
    fl = [3514, 763, 1011, 1762, 8012, 7513, 4515, 8760, 1263, 8512, 14, 7011, 2013, 2514, 6762, 10012, 7262, 264, 9512, 5263, 9310, 2310, 3555, 8551, 60, 4806, 1303, 562, 6314, 1563, 3065, 5306, 9067, 8055,
          7303, 7061, 5557, 2558, 1053, 307, 9600, 1849, 6352, 106, 5859, 4365, 4846, 8090, 4115, 6850, 6604, 7340, 8840, 8583, 856, 3107, 4599, 7593, 8357, 3599, 6172, 7966, 8425, 8967, 5737, 8737, 8242, 7748, 6495]
    lines2 = [lines[i] for i in fl]
    threads = []
    for i in range(0, 1):
        threads.append(Thread(target=downLoadHtmlPageThread, args=(
            lines2, 0, len(lines2))))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# allReviewLinkExtractor()
# uniqueReviewLinkExtractor()
# gameLinkExtractor()
# failedLinkExtractor()
# gameSpotLinkCombiner()
# downLoadHtmlPage()
# downLoadFailedHtmlPage()
