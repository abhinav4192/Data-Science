from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
from threading import Thread
import re
import urllib.request
import requests
import os
from os.path import isfile, join


def downLoadHtmlPageThread(start, end):
    quote_page = "https://howlongtobeat.com/game.php?id="
    for i in range(start, end):
        print("trying for number:", i)
        qp = quote_page + str(i)
        try:
            r = requests.get(qp).text
            soup = BeautifulSoup(r, "lxml")
            if soup.title.get_text() == "How long does it take to beat your favorite games? - HowLongToBeat.com":
                continue
            fileName = '../hltb_HTML/' + \
                re.sub(r'\W+', '', "_".join(soup.title.get_text().split(' - HLTB')
                                            [-2].split()[3:])) + ".html"
            f = open(fileName, 'w+')
            f.write(str(soup))
            f.close()
        except:
            print("Failed for number:", i)
            time.sleep(15)


# method to download html pages from "how long to beat"
def downLoadHtmlPage():
    threads = []
    for i in range(0, 50):
        threads.append(Thread(target=downLoadHtmlPageThread, args=(i * 1000, (i + 1) * 1000)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def getAllFiles(folderName):
    filePaths = []
    for fileName in sorted(os.listdir(folderName)):
        fileName = join(folderName, fileName)
        if fileName.endswith('.html') and isfile(fileName):
            filePaths.append(fileName)
    return filePaths


# Keep only valid pages with valid games
def cleanFolder():
    files = getAllFiles('../hltb_HTML')
    for f in files:
        with open(f) as fp:
            soup = BeautifulSoup(fp, 'lxml')
            mydivs = soup.find("div", {"class": "profile_details"})
            items = mydivs.text.split('\n')
            for li in items:
                if len(li) < 4:
                    continue
                kv = li.split(' ')
                key = kv[1]
                val = kv[0]
                try:
                    if key == "Rating":
                        if val == "NR":
                            print("removed:", f)
                            os.remove(f)
                            break
                    elif key == "Beat":
                        if float(val) < 10:
                            print("removed:", f)
                            os.remove(f)
                            break
                except:
                    pass


# downLoadHtmlPage()
# cleanFolder()
