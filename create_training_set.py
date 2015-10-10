'''

This file will create the training set for training the neural net that can categorize the books.

Assumption: 
    The Book pdfs are stored in some directory. That directory is assigned to the global source_dir.
    The pdfs are named as {ISBN}.*
    Using the isbn and the google books api the metadata of the book is looked up.

'''

import os
import json
import urllib2

source_dir = '/home/utpal/Downloads/ToCat/'
output_dir = '/home/utpal/bcnn/json/'
replacements = [ (':', ' - '), (' and ', ' & '), ('/', '-')]
API_KEY = 'AIzaSyAbPoAtWdCPp3rXF9bII3WJX3q2SbF_tdo'

def cleanTitle(title, extensionPart, isbn):
    if len(title) != 0 and not title.endswith(extensionPart):
        title = title.title() + '_' + isbn + extensionPart

    for item in replacements:
        title = title.replace(item[0], item[1])
    return title

if __name__ == '__main__':
    for filename in os.listdir(source_dir):
        if os.path.isfile(source_dir + filename):
            # parse the filename
            filenamePart, extensionPart = os.path.splitext(filename)     
            isbn = filename[0:10]
            print filenamePart, isbn
            output_file_name = output_dir + isbn + '.json'
            # if the output file name exists then we have already got this object. 
            if not os.path.isfile(output_file_name):
                url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn + '&key=' + API_KEY 
                print url
                jo = json.load(urllib2.urlopen(url))
                # check if we did get a valid json
                if 'items' in jo:                    
                    print 'Obtained json. ', output_file_name
                    f = open(output_file_name, 'w')
                    f.write(json.dumps(jo))
                    f.close()
                    if len(jo['items']) == 1:
                        iteminfo = jo['items'][0]['volumeInfo']
                        #print iteminfo
                        if 'title' in iteminfo:
                            title = iteminfo['title']
                            title = cleanTitle(title, extensionPart, isbn)
                            print "Obtained Title: " + title
                            print "For file: " + filename
                            choice = raw_input("Rename?(y/n)")
                            if choice == 'y':
                                os.rename(source_dir + filename, source_dir + title)
                                print 'renamed'
