import requests, csv
import pprint as pr

basesearch = "https://api.scryfall.com/cards/search?q="

def prep_csv(filepath):
    file = open(filepath)
    csvreader = csv.reader(file)

    rows = []
    for row in csvreader:
        rows.append(row)

    file.close()

    print('Preparing CSV list...')
    collection = []
    for card in rows:
        indx_1 = card[0].find('\t',1)
        indx_2 = card[0].find('\t',3)
        collection.append(card[0][indx_1 + 1 : indx_2])

    return collection

def main(csvfilepath):
    searchterms = []
    searchURL = ''

    collection = prep_csv(csvfilepath)
    
    print('Please make sure all searches use the scryfall search syntax.')
    while True:
        print('Type "help" for assistance')
        inpt = input('Please input your terms: ').lower()

        if inpt == 'help':
            print('AVALIABLE COMMANDS:')
            print('done - once all terms have been added')
            print('quit - exit the program')
            
        if inpt == 'quit':
            exit()

        if inpt == 'done':
            break

        else:
            searchterms.append(inpt)

    
    print('Assembling search...')
 
    searchURL += "+".join(searchterms)

    print('Final search link:', searchURL)

    #Query Scryfall for our search
    response = requests.get(basesearch + searchURL)

    if response.status_code != 200:
        print('ERROR, Status Code: 200')
        input('Press Enter to exit...')
        exit()

    results = response.json()
    results_list = results['data']
  
    for cardresult in results_list:
        if cardresult['name'] in collection:
            print(cardresult['name'])
             
main('All_cards.csv')
input('Press enter to exit...')
