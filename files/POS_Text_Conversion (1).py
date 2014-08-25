
# coding: utf-8

## Examples of Tokenizing, Cleaning, Rewriting with Parts of Speech

##### This notebook assumes you installed nltk and pattern already. (@arnicas, Aug 2014)

import os
from pattern.en import tag as ptag
import ununicode
import string
import sys

def print_all_tags(text):
    for word, tag in ptag(text):
        print word, tag

# Make it more general - pass in the Part of Speech you want
def tag_by_line(line, tag):
    # matching the first two chars of the tag - so verbs are vb, etc.
    words = []
    for word,foundtag in ptag(line):
        if foundtag[0:2]== tag:  # first 2 chars are the base tag
            words.append(word)
    return words

def cleanup(text):
    """ This function cleans up the text a bit, and removes newlines."""

    data = text.decode('utf8')
    data = ununicode.toascii(data)  # a useful function that does some simple unicode replacements
    data = data.replace('\r', '')  # windows newline in some files
    data = data.replace('\n', ' ')  # turn newline into space
    data = data.strip()  # strip remaining white space chars from edges
    return data


def cleanup_and_pos(text, pos='VB'):
    """ Run the cleanup function, convert to a list of verbs, clean out misc stuff left."""

    other_things_to_strip = []  # put your own list of strings here, based on reading outputs

    data = cleanup(text)
    verbs = tag_by_line(data, pos)   # returns a list of verbs
    cleanverbs = [verb for verb in verbs if verb not in string.punctuation]
    cleanverbs = [word for word in cleanverbs if word not in other_things_to_strip]
    newdata = ' '.join(cleanverbs)  # make it a single string
    return newdata


def rewrite_all(dirname, newdir, funct=cleanup_and_pos, pos='VB'):
    """ Take in a director of original docs, a new directory name, and a function to apply to each."""

    if not os.path.exists(newdir):
        print 'Making directory', newdir
        os.makedirs(newdir)

    for (dirpath, dirname, filenames) in os.walk(dirname):
        for file in filenames:
            print dirpath, file
            with open(os.path.join(dirpath,file), 'r') as myfile:
                data=myfile.read()
                newdata = funct(data, pos=pos)
                newfilename = os.path.basename(file)
                with open(os.path.join(newdir, newfilename), 'wb') as temp_file:
                    temp_file.write(newdata.encode('utf8'))
                    print 'Wrote ', os.path.join(newdir, newfilename)





def main():
    if len(sys.argv) != 4:
        print 'Usage: preprocess_files original_dir new_dir part_of_speech'
    else:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
        POS = sys.argv[3]

        rewrite_all(input_dir, output_dir, funct=cleanup_and_pos, pos=POS)
        print 'Wrote out new files to ', output_dir

if __name__ == "__main__":
    main()
