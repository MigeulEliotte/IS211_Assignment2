import argparse
import urllib.request
import logging
import datetime
import csv

def downloadData(url):
    """Downloads the data"""
    return urllib.request.urlopen(url).read().decode('utf-8')

def processData(file_content):
    """This processes the CSV data and logs errors"""
    data_dict = {}
    logger = logging.getLogger('assignment2')
    csv_reader = csv.reader(file_content.splitlines())
    

    for linenum, row in enumerate(csv_reader, start=1):

        person_id, name, birthday = row
        try:
            birthday = datetime.datetime.strptime(birthday, '%d/%m/%Y').date()
            data_dict[int(person_id)] = (name, birthday)
        except ValueError:
            logger.error(f"Error processing line #{linenum} for ID #{person_id}")
    
    return data_dict
#this communicates with the user
def displayPerson(id, personData):
    """Display someone's information by ID number"""
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday}")
    else:
        print("ID Not Found")

def setupLogger():
    """Sets up logging configuration"""
    logging.basicConfig(filename='errors.log', level=logging.ERROR)

def main(url):
    print(f"Running main with URL = {url}...")
    setupLogger()



    # this downloads the data
    try:
        csv_data = downloadData(url)
    except urllib.error.URLError as e:
        print(f"Failed to retrieve data: {e}")
        return

    # Process data
    person_data = processData(csv_data)
    
    # Ask for user input
    while True:
        try:
            user_input = int(input("Enter an ID # for lookup (negative number to exit): "))
            if user_input <= 0:
                break
            displayPerson(user_input, person_data)
        except ValueError:
            print("Please enter a Valid Number.")



if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
