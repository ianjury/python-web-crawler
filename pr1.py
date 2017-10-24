"""
Ian Jury
TCSS 480 Fall 2017
Assignment 1
"""
import re
import urllib.request


def process_web_page(url, count, already_visited_pages, total_word_list):
    if count < 50:  # limits web page visiting to 50, as specified in requirements
        page = urllib.request.urlopen(url)
        page_text = str(page.read())
        links = re.findall(r'a href[\s+]?=[\s+]?["]?([^"\s >]+)', page_text)  # gets absolute urls in current page
        links = list(set(links))  # make links unique, just in case they are reference multiple times.
        write_connections_to_csv(url, links)

        total_word_list += re.findall('<[hp][1-9]?>(.*?)</[hp][1-9]?>', page_text)  # get text
        #print(total_word_list)

        for sub_url in links:  # for each url, visit the children urls
            if sub_url not in already_visited_pages:
                count += 1
                already_visited_pages.append(sub_url)  # remember which pages have already been visited (prevent loops)
                process_web_page(sub_url, count, already_visited_pages, total_word_list)  # recursively crawl through child pages
                # print(sub_url, count)
        # print(alreadyVisitedPages)
    else:
        print('Exceeded 50 sites.')

    return total_word_list


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

def analyze_words(word_list):
    word_dict = {}
    for sentence in word_list:
        for word in sentence.split():
            word = word.rstrip(r'],.')
            print(word)


# clears csv file, and starts the crawling process on each of the provided links.
def main():
    open('results.csv', 'w').close()  # clear contents of csv from previous executions of the program
    test_files = ['urls2.txt', 'urls3.txt', 'urls6.txt']  # holds names of test files provided
    url_list_file = open(test_files[0], 'r')  # change index here to go between test files.
    url_list = []
    for url in url_list_file:  # get list of urls in file
        url = url.rstrip() # remove newline
        url_list.append(url)
        word_list = process_web_page(url, 0, [url], [])  # gets all of the 'text' words from the html files
        analyze_words(word_list)
        print(word_list)

    url_list_file.close()


if __name__ == "__main__":
    main()
