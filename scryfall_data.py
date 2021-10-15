#shadowfray
#Scryfall data connector

import requests, sql_scry, time, csv
import pprint as pr

from datetime import date

def main():
    #TO DO: Add interace to pick a deck / add a deck / etc

    #adds price of a deck to the file with deck_id = 1
    priceFetcher(1, 'EDHCostTrend.db')

def priceFetcher(deckID:int,    #The integer assigned to all cards in this deck for the database
                 dbFile:str     #The name of the SQLite databse to be used
                 ):

    #returns the cards from the database
    card_list = sql_scry.fetchCards(sql_scry.create_connection(dbFile), deckID)

    #returns the date reformated for the SQL database
    today = str(date.today())
    todayList = list(today)
    
    for i in todayList:
        if i == '-':
            pos = todayList.index(i)
            todayList[pos] = '_'
            
    today = ''.join(todayList)

    #creates the daily column
    con = sql_scry.create_connection(dbFile)
    sql_scry.add_column(con, 'prices', today, 'REAL') 

    #to place the prices returned
    price_list= []
    id_list = []

    #THE CONNECTION
    results_list = scryConnect(card_list)

    for i in results_list:
        price_list.append(i[0]['prices']['usd'])
        id_list.append(i[0]['oracle_id'])

    sql_scry.add_values(con, price_list, id_list, 'prices', today)

#calls Scryfall.com for information of each card in card_list using Scryfall API
def scryConnect(card_list):
    #the connection
    return_list = []
    
    for cardName in card_list:
        time.sleep(.2) #rate limiter
        response = requests.get(f'https://api.scryfall.com/cards/search?q=!"{cardName}"')

        if response.status_code != 200:
            return None

        results = response.json()
        results_list = results['data']
        return_list.append(results_list)

    return return_list
        
#adds the cards in the SQL database
def deckListAdd(filepath, deckID: int):
    deckList = returnCSVList(filepath)
    deckName = filepath[:-4]

    #a list of all the cards
    cardNames = []
    for i in deckList:
        cardNames.append(f'"{i[2]}"')

    #gathers & creates a list of the card IDs   
    results = scryConnect(cardNames)
    id_list = []

    for i in range(len(results)):
        id_list.append(f'"{results[i][0]["oracle_id"]}"')

    sql_scry.add_deck(sql_scry.create_connection('EDHCostTrend.db'), cardNames, deckID, id_list, deckName)

#returns CSV file as a series lists within a list
def returnCSVList(filename):
    file = open(filename)
    deckReader = csv.reader(file)
    deckList = list(deckReader)[1:]

    return deckList

#prints a deck given a list for easy reading
def printDeck(decklist):
    for i in decklist:
        print(i[1],i[2])
main()


