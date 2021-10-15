#Shadowfray
#SQLite3 connector program

import sqlite3

#creates a connection with a database
def create_connection(datab_file):
    connection = None
    
    try:
        connection = sqlite3.connect(datab_file)
    except Error as e:
        print(e)

    return connection

#adds a new column to the database for that day's price info
def add_column(connection, tableName, columnName, typeData):
    c = connection.cursor()
    
    sql = f'ALTER TABLE {tableName} ADD COLUMN "{columnName}" {typeData}'

    #does not create a column for that day if it already exists
    try:
        c.execute(sql)
        connection.commit()
        print('added')
    except Exception as e:
        print(e)

    c.close()

#adds the new values into the new column
def add_values(connection, values:list, card_ids:list, tableName, columnName, idFilter=True):
    c = connection.cursor()
    
    for i in range(len(values)):
        print(card_ids[i])
        
        sql = f'''UPDATE {tableName}
                SET "{columnName}" = {values[i]}
                WHERE card_id =  "{card_ids[i]}"
                '''
        try:
            c.execute(sql)
            connection.commit()
        except Exception as e:
            print('Er (add_values):', e)
    c.close()

#adds a new deck into deck_list in the SQL file with the appropriate IDs and names
def add_deck(connection, cardnames:list, deckID:int, card_ids:list, deckName:str):
    c = connection.cursor()

    #adds each card with the deck ID and card ID
    for i in range(len(cardnames)):
        sql = f'''INSERT INTO deck_lists (cardname, deck_id, card_id)
                VALUES ({cardnames[i]}, {deckID}, {card_ids[i]});'''
        try:
            c.execute(sql)
            connection.commit()
        except Exception as e:
            print(e)

    #adds the deck to the deck list w/ the deck ID
    sql = f'INSERT INTO decks (deck_name, deck_id) VALUES ("{deckName}", {deckID})'
    c.execute(sql)
    connection.commit()

    #adds the IDs into the prices table
    for i in range(len(card_ids)):
        sql = f'INSERT INTO prices (card_id) VALUES ({card_ids[i]})'
        c.execute(sql)
        connection.commit()
    
    c.close()

#takes a deck ID and returns all cards in that deck
def fetchCards(connection, deckID:int):
    deckList = []
    c = connection.cursor()

    c.execute(f'SELECT cardname FROM deck_lists WHERE deck_id = {deckID}')
    cards = c.fetchall()

    #places them into deckList, removing the tuples
    for i in cards:
        deckList.append(i[0])

    return deckList
