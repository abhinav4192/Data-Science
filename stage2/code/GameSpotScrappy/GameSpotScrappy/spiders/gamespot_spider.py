import scrapy
import logging
import os
from os.path import isfile, join
import sys


def getAllFiles(folderName):
    filePaths = []
    for fileName in sorted(os.listdir(folderName)):
        fileName = join(folderName, fileName)
        if fileName.endswith('.html') and isfile(fileName):
            filePaths.append(fileName)
    print(len(filePaths))
    return filePaths


class GamespotSpider(scrapy.Spider):
    name = "gamespot"
    start_urls = ['file://' +
                  f for f in getAllFiles('/Users/abhinavgarg/DataScience/gameSpot_HTML')]
    counter = 0
    custom_settings = {
        'LOG_LEVEL': logging.CRITICAL,
    }

    def parse(self, response):

        self.counter += 1
        if self.counter % 100 == 0:
            print('.', end='')
            sys.stdout.flush()

        keys = ["Title", "Developer", "Publisher", "Platform", "Genre", "ReleaseDate", "Rating"]
        game_details = {"Title": "", "Developer": "", "Publisher": "",
                        "Platform": "", "Genre": "", "ReleaseDate": "", "Rating": ""}

        gsTitle = response.xpath(
            '//dl[@class="pod-objectStats-info"]/dt/h3/a[contains(@data-event-tracking,"Title")]/text()').extract_first()
        gsRelease = response.css('dd.pod-objectStats-info__release').re_first(r'<span>*(.*)</span>')
        gsPlatform = response.xpath(
            '//dd[@class="pod-objectStats-info__systems"]/ul[@class="system-list"]/li/text()').extract()
        gsUserRating = response.xpath(
            '//dt/a[contains(@data-event-tracking,"UserReviewScore")]/text()').extract_first()

        gsMetaDiv = response.xpath('//dl[@class="pod-objectStats-additional"]')
        gsDev = gsMetaDiv.xpath(
            '//dd/a[contains(@data-event-tracking,"Developer")]/text()').extract()
        gsPub = gsMetaDiv.xpath(
            '//dd/a[contains(@data-event-tracking,"Publisher")]/text()').extract()
        gsMetaGenre = gsMetaDiv.xpath(
            '//dd/a[contains(@data-event-tracking,"Genre")]/text()').extract()

        game_details["Title"] = gsTitle.strip()
        game_details["ReleaseDate"] = gsRelease.strip()
        game_details["Platform"] = ",".join(gsPlatform)
        game_details["Rating"] = gsUserRating
        game_details["Developer"] = ",".join(gsDev)
        game_details["Publisher"] = ",".join(gsPub)
        game_details["Genre"] = ",".join(gsMetaGenre)
        try:
            f, game_details = cleanData(game_details)
            if f:
                yield game_details
        except Exception as e:
            print("Exception", e)


def cleanData(game_details):
    for k in ["Title", "Developer", "Publisher", "Platform", "Genre", "ReleaseDate"]:
        try:
            game_details[k].encode('ascii')
        except:
            print("ASCII Encoding failed")
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

    if game_details['Rating'] != None:
        game_details['Rating'] = float(game_details['Rating'])
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
