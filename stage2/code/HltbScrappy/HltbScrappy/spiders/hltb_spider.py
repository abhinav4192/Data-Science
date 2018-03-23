import scrapy
import logging
import os
from os.path import isfile, join
import re
import sys


def getAllFiles(folderName):
    filePaths = []
    for fileName in sorted(os.listdir(folderName)):
        fileName = join(folderName, fileName)
        if fileName.endswith('.html') and isfile(fileName):
            filePaths.append(fileName)
    print(len(filePaths))
    return filePaths


class HltbSpider(scrapy.Spider):
    name = "hltb"
    start_urls = ['file://' + f for f in getAllFiles('/Users/abhinavgarg/DataScience/hltb_HTML')]

    custom_settings = {
        'LOG_LEVEL': logging.CRITICAL,
    }
    counter = 0

    def parse(self, response):

        self.counter += 1
        if self.counter % 100 == 0:
            print('.', end='')
            sys.stdout.flush()

        keys = ["Title", "Developer", "Publisher", "Platform", "Genre", "ReleaseDate", "Rating"]
        game_details = {"Title": "", "Developer": "", "Publisher": "",
                        "Platform": "", "Genre": "", "ReleaseDate": "", "Rating": ""}
        game_details["Title"] = response.xpath(
            '//div[@class="profile_header shadow_text"]/text()').extract_first().strip()

        game_profile = response.xpath('//div[@class="profile_info"]').extract()
        regex = re.compile(".*>.*>(.*)<.*>(.*)<.*")
        for p in game_profile:
            p = p.replace("\n", "").strip()
            try:
                searchObj = re.search(regex, p)
                if searchObj != None:
                    if(searchObj.group(1).strip().startswith("Dev")):
                        game_details["Developer"] = searchObj.group(2).strip()
                    elif(searchObj.group(1).strip().startswith("Pub")):
                        game_details["Publisher"] = searchObj.group(2).strip()
                    elif(searchObj.group(1).strip().startswith("Playable")):
                        game_details["Platform"] = searchObj.group(2).strip()
                    elif(searchObj.group(1).strip().startswith("Genre")):
                        game_details["Genre"] = searchObj.group(2).strip()
                    elif(searchObj.group(1).startswith("NA")):
                        game_details["ReleaseDate"] = searchObj.group(2).strip()
            except Exception as e:
                print(str(e))

        rating_details = response.xpath('//div[@class="profile_details"]/li').extract()
        regex = re.compile(".*>(.*)<.*><.*><.*>(.*)<.*")
        for d in rating_details:
            d = d.replace("\n", "").strip()
            try:
                searchObj = re.search(regex, d)
                if searchObj != None:
                    if(searchObj.group(2).strip() == "Rating"):
                        game_details["Rating"] = searchObj.group(1).strip().replace("%", "")
                        break
            except Exception as e:
                print(str(e))
        f, game_details = cleanData(game_details)
        if f:
            yield game_details


def cleanData(game_details):
    for k in ["Title", "Developer", "Publisher", "Platform", "Genre", "ReleaseDate"]:
        try:
            game_details[k].encode('ascii')
        except:
            return False, game_details

    keys = ["Title", "Developer", "Publisher", "Platform", "Genre", "ReleaseDate", "Rating"]

    if len(game_details['Title']) == 0:
        return False, game_details
    game_details['Title'] = game_details['Title'].strip().replace(", ", " ").replace(",", "")

    if len(game_details['ReleaseDate']) != 0:
        game_details['ReleaseDate'] = game_details['ReleaseDate'].replace(",", "")
        g = game_details['ReleaseDate'].split(' ')
        if len(g) == 3:
            game_details['ReleaseDate'] = g[1] + " " + g[0] + " " + g[2]

    for k in ["Developer", "Publisher", "Platform", "Genre"]:
        game_details[k] = handleCommaSeperatedValues(game_details[k])

    if len(game_details['Rating']) != 0:
        game_details['Rating'] = int(game_details['Rating']) / float(10)
    return True, game_details


def handleCommaSeperatedValues(s):
    if len(s) == 0:
        return s
    s = s.strip()
    g = s.split(',')
    for i in range(0, len(g)):
        g[i] = g[i].strip()
    s = "|".join(g)
    return s
