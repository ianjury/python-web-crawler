"""
Ian Jury
TCSS 480 Fall 2017
Assignment 1
"""
import re
import urllib.request
from tkinter import *
import random
from multiprocessing import Pool


# Shouldn't use global variables - but was running into problems with recursive calls in method below.
c = 0

#
def process_web_page(url, already_visited_pages, total_word_list):
    global c
    print('analyzing web page...')
    if c < 50:  # limits web page visiting to 50, as specified in requirements
        #print(url)
        try:  # prevents hitting dead 404 webpage
            c += 1
            page = urllib.request.urlopen(url)
            page_text = str(page.read())
            links = re.findall(r'a href[\s+]?=[\s+]?["]?(http[^"\s >]+)', page_text)  # gets absolute urls in current page
            links = list(set(links))  # make links unique, just in case they are reference multiple times.
            write_connections_to_csv(url, links)

            total_word_list += re.findall('<[hp][1-9]?>[^<](.*?)</[hp][1-9]?>', page_text)  # get text
            #print(total_word_list)

            for sub_url in links:  # for each url, visit the children urls
                if sub_url not in already_visited_pages:
                    already_visited_pages.append(sub_url)  # remember which pages have already been visited (prevent loops)
                    process_web_page(sub_url, already_visited_pages, total_word_list)  # recursively crawl through child pages
        except:
            pass
        # print(alreadyVisitedPages)
    else:
        # print('Exceeded 50 sites.')
        return None

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


# Takes list of words and converts and returns a dictionary where the key = word, value = count
def analyze_words(word_list):
    word_dict = {}
    for sentence in word_list:
        for word in sentence.split():
            word = word.rstrip(r"]],.}")  # Strip non alpha chars
            word = word.lstrip(".'[{")
            word = word.lower()
            if word in word_dict:  # If already in dictionary, increment associated value counter
                word_dict[word] += 1
            else:
                word_dict[word] = 1  # Else, initialize counter

    return word_dict


# creates and displays word cloud using word frequency dictionary -- current word cloud count == 12
def create_word_cloud(word_dict):
    gui = Tk()
    dim = 500
    gui.geometry('500x500+300+200')
    font_size = 45
    previous_starting_points = []  # The previous starting point for words so they're not drawn over each other
    for count in range(12):
        if word_dict:  # Checks that there are still words in the dictionary
            current_largest = max(word_dict, key=word_dict.get)

            T = Text(gui, height=1, width=30)
            T.pack()
            T.config(font=("Courier", font_size))

            starting_point = random.randrange(0,15)  # randomly assign starting point for word placement
            while starting_point in previous_starting_points:  # but don't allow overlapping words
                starting_point = random.randrange(1, 15)
            T.grid(row = starting_point)
            T.insert(END, current_largest)

            previous_starting_points.append(starting_point)  # Housekeeping
            del word_dict[current_largest]
            font_size -= 3
        else:  # If there are less than 12 unique words, then we're just going to get out.
            print("Less than 12 unique words found in pages")
            break
    print('View GUI for results.')
    gui.mainloop()


# clears csv file, and starts the crawling process on each of the provided links.
def main():

    open('results.csv', 'w').close()  # clear contents of csv from previous executions of the program
    test_files = ['urls2.txt', 'urls3.txt', 'urls6.txt']  # holds names of test files provided

    url_list_file = open(test_files[2], 'r')  # change index here to go between test files.

    url_list = []
    word_lists = []
    for url in url_list_file:  # get list of urls in file
        url = url.rstrip()  # remove newline
        url_list.append(url)
        global c
        c = 0
        word_lists.append(process_web_page(url, [url], []))  # gets all of the 'text' words from the html files
    '''Processes the list of words found using multithreading, so each word could is ready to be displayed,
       and stores all of the results in a list of dictionaries.
       TKinter wouldn't allow multiple instances of a GUI in multiprocessing (although there is probably a
       workaround), so only one will be displayed at a time, but the processing for each is finished at the same time.   
    '''
    pool = Pool()
    word_dicts = pool.map(analyze_words, word_lists) # Processes all of the word lists

    for r in word_dicts:
        create_word_cloud(r)

    url_list_file.close()


if __name__ == "__main__":
    main()
