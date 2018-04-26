'''
Ronald Pastori
Overwatch Web Crawler
'''

import os
import requests # Must be installed with pip3 in the command line
import sys
from pathlib import Path
from urllib.parse import urlparse

usage = lambda msg: print(msg, file = sys.stderr)

argc = len(sys.argv)

# Cleanly handles arguments for the sake of modularity and a clean main.
# Very basic functionality for now. I plan on implementing a smarter arg handler
# That can accomodate several different ways the user may pass parameters.
def fetchArgs():
    if argc == 3:
        seedList = sys.argv[1].strip('[]"\'').split(',')
        termList = sys.argv[2].strip('[]"\'').split(',')

        for i in range(len(seedList)):
            seedList[i] = seedList[i].strip(' ')
            if not bool(urlparse.urlparse(seedList[i]).scheme):
                usage("URL list argument contains an invalid URL.")
                return None, None

        for i in range(len(termList)):
            termList[i] = termList[i].strip(' ')

        return seedList, termList
    elif argc == 13: # In the case people enter 12 strings instead of 2 lists
        seedList = []
        termList = []
        for i in range(1, 13):
            arg = sys.argv[i].strip('[]"\', ')
            if i in (1,2):
                seedList.append(arg)
            else:
                termList.append(arg)
        return seedList, termList
    else:
        usage(
            "Please enter two arguments: [list of seed URLS] | [list of ten related terms]"
            )

def getPlayerName(url):
    page = requests.get(url)
    print(page)

def crawl(seedURL, teamIDs, folderPath):
    queue = []
    visited = []
    crawledCount = 0
    limit = 200
    baseUrl = 'https://www.winstonslab.com/'
    playerPiece = 'players/player.php?id='
    for id in teamIDs: # Generates URLs for all OWL team pages
        queue.append(seedURL + id)

    print("Starting the webcrawl process:")
    print("... crawling...")
    while queue and crawledCount < limit: # While the queue is not empty
        currURL = queue.pop(0)
        if currURL not in visited:
            resp = requests.get(currURL)
            visited.append(currURL)

            # Checks if current page is a player page
            player = False
            if currURL[:50] == baseUrl + playerPiece:
                player = True

            playerName = getPlayerName(currURL)
            if player:
                # save to directory
                # Maybe replace page# with player name
                getPlayerName(currURL)
                '''with open(str(folderPath) + '/page' + str(crawledCount) + '.html', 'w') as o:
                    o.write(resp.text)
                crawledCount += 1
                '''
            # Looks for new URLs linked in the page.
            # For now, I'm limited to Wikipedia pages, which makes my job easier
            pageLocation = 'href="/players/player.php?id='
            for line in resp.iter_lines():
                idx = str(line).find(pageLocation)
                if idx != -1:
                    urlPiece = str(line)[idx + len(pageLocation):] # slice of line
                    tempList = urlPiece.split('"') # separates the player ID
                    urlPiece = tempList[0] # from the trailing junk
                    queue.append(baseUrl + playerPiece + urlPiece)
        crawledCount += 1
    print("All done!")

def main():
    seedURL = "https://www.winstonslab.com/teams/team.php?id="
    # Team IDs for all S1 OWL teams
    teamIDs = ['318', '328', '329', '330', '331', '332', '333', '334', '335', '336', '337', '338']
    folderPath = Path('/pages')

    if argc > 1:
        seedURL, teamIDs = fetchArgs()
        if seedURL is None or teamIDs is None:
            return

    crawl(seedURL, teamIDs, folderPath)

main()
