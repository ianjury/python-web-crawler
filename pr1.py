"""
Ian Jury
TCSS 480 Fall 2017
Assignment 1
"""
import re
import urllib.request


def process_web_page(url, count, alreadyVisitedPages):
    if count < 50:
        page = urllib.request.urlopen(url)
        page_text = str(page.read())
        links = re.findall(r'a href[\s+]?=[\s+]?["]?([^"\s >]+)', page_text) #get all absolute urls
        links = list(set(links)) # make links unique, just in case they are reference multiple times.
        write_connections_to_csv(url, links)

        for sub_url in links:  # for each url, visit the children urls
            if sub_url not in alreadyVisitedPages:
                count += 1
                alreadyVisitedPages.append(sub_url)
                process_web_page(sub_url, count, alreadyVisitedPages)
                #print(sub_url, count)
        #print(alreadyVisitedPages)
    else:
        print('Exceeded 50 sites.')


# Writes url and link connections to csv file.
def write_connections_to_csv(url, links):
    f = open('results.csv', "a+")
    write_string = url + ','
    for connections in links:
        write_string += connections + ','
    write_string.rstrip(',')
    write_string += '\n'
    # print(write_string)
    f.write(write_string)

    f.close()


def main():
    open('results.csv', 'w').close()  # clear contents of csv from previous executions of the program
    test_files = ['urls2.txt', 'urls3.txt', 'urls6.txt']  # holds names of test files provided
    url_list_file = open(test_files[0], 'r')  # change index here to go between test files.
    url_list = []
    for url in url_list_file:  # get list of urls in file
        url = url.rstrip() # remove newline
        url_list.append(url)
        process_web_page(url, 0, [url])

    url_list_file.close()


if __name__ == "__main__":
    #  sys.setrecursionlimit(50)  # Since we only want to visit 50 pages, we set the recursion limit here.
    main()
