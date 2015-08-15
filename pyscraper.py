import sys
import pandas
from urllib2 import urlopen, URLError
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

def parse_arguments():
    """ Process command line arguments """
    parser = ArgumentParser(description='Grabs tables from html')
    parser.add_argument('-u', '--url', help='url to grab from',
                        required=False)
    args = parser.parse_args()
    return args


def parse_rows(rows):
    """ Get data from rows """
    results = []
    for row in rows:
        table_headers = row.find_all('th')
        if table_headers:
            results.append([headers.get_text() for headers in table_headers])

        table_data = row.find_all('td')
        if table_data:
            results.append([data.get_text() for data in table_data])
    return results

def parse_array(array, num):
    """ Get individual data from rows array"""
    array_data = []
    array_data += [row[num] for row in array]
    array_data.remove(array_data[0])
    return array_data



@app.route('/', methods=['GET', 'POST'])
def index(arrayString=""):
    return render_template('index.html', arrayString = arrayString)

def main():
    args = parse_arguments()

    # Retrieving URL and reading the HTML
    try:
        resp = urlopen('http://famat.org/Downloadable/Results/State%202015/Theta%20Individual_Indv.html')
    except URLError as e:
        print 'An error occured fetching %s \n %s' % (url, e.reason)   
        return 1
    soup = BeautifulSoup(resp.read(), "lxml")

    # Get table
    try:
        table = soup.find('table')
        rows = table.find_all('tr')
    except AttributeError as e:
        raise ValueError('No valid table found')

    table_data = parse_rows(rows)

    school = parse_array(table_data, 1)
    student = parse_array(table_data, 2)
    score = parse_array(table_data, 3)
    student_id = parse_array(table_data, 4)
    num_right = parse_array(table_data, 5)
    num_wrong = parse_array(table_data, 6)
    num_blank = parse_array(table_data, 7)
    t_score = parse_array(table_data, 8)

    # Print table data
    # with open('test.txt', 'w') as f:
    #     for i in table_data:
    #         #print '\t'.join(i)
    #         f.write("%s\n" % str('\t'.join(i)))/
    scoreString = ' '.join(score)

    columns = ["a", "b", "c", "d", "e", "f", "g", "h"] #a csv with 8 columns
    index = [i[0] for i in table_data] #first element of every list in yourlist
    not_index_list = [i[1:] for i in table_data]
    pd = pandas.DataFrame(not_index_list, columns = columns, index = index)

    #Now you have a csv with columns and index:
    pd.to_csv("mylist.csv")

    # with open('test.txt', 'w') as f:
    #     for word in schoolString.split("  "):
    #         f.write("%s\n" % str(word))

    arrayString = ""
    arrayString += scoreString
    # for i in table_data:
    #    arrayString += '\t'.join(i)

    return arrayString

if __name__ == '__main__':
    #status = main()
    app.run(debug=True)
    #sys.exit(status)