# EDH-PriceTracker-ScryfallAPI
A program that gathers data from Scryfall via API and compiles card prices into a SQLite data base.

This program is to be used to gather data on card prices from Magic: The Gathering of an EDH deck off the website Scryfall via their API. It then takes this data and
adds it into an SQL database so that the card prices can be examined in the long run over a period of time.

It is designed to take a deck list in a .csv file, probably downloaded from Tappedout.com, then upload it into the database.

As of now it works with a file called EDHCostTrend.db, but that can easily be changed. For now main() simply has a preset function to call but that can be edited as needed.

The deckListAdd() function is needed to first add the deck to the database, as otherwise the rest of the code will not know what to do, as the card's ID is used as a reference.

The database consists of three tables:

deck_lists: comprised of three columns,
    -cardname: the name of the card. Not unique, see deck_id
    -deck_id: the number that tells you which deck this is in. Not unique.
                TO DO: Handle a card in multiple decks properly
    -card_id: The unique identifier of each card used. This is the ID that
        Oracle uses for each card, and is gathered via Scryfall,

decks: the list of EDH decks stored,
    -deck_name: the name of the deck, the name of the .csv file used
    -deck_id: same as in deck_lists, used to connect

prices: the prices of each card,
    -card_id: see deck_lists, used to connect
    -*addtional columns*: The program will add additional columns to note the
        price whenever it is run. This column is named after the date it is
        created, formatted via the datetime module, but with underscores.


While scryfall_data gathers data via Scryfall API and extracts it, the file sql_scry contains all the functions used to interface with the database via SQLite3.

The database provided already has one deck imported and one date of data to serve as an example.
