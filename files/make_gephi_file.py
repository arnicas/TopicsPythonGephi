
"""
Usage: python make_gephi_file.py [csv_directory] [optl label]
Directory is the dir of the Mallet GUI output csv files,
label is an optional label to append to your output files so you
can tell them apart. (@arnicas, Aug 2014)
"""

import csv
import sys

# pass in the topic_words filename
# This will give you the 10 words per topic; we asked for 10 topics
def list_words_for_topics(filename):
    """ Pass in the Topics_Words csv file."""
    words = {}
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for index, row in enumerate(spamreader):
            if index > 0:  # skip first row
                words[row[0]] = [x.strip() for x in row[1].split() if len(x.strip())>0]
                #print row
    return words

def get_names_for_ids(filename):
    """
    Pass in the Docs in Topics csv file.
    Get out 2 data dictionaries, the file titles and authors, from the filename
    """
    doc_titles = {}  # dictionary, the keys will be the doc id, the filename the value
    doc_authors = {}
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for index, row in enumerate(spamreader):
            #print row
            if index > 0:  # skip first row making the data structure
                title = row[3].split('/')[-1:][0]  # last element of the split
                author = title.split('_')[0]
                id = row[2]
                #print "Parsed out ", title, author
                doc_titles[id] = title
                doc_authors[id] = author
    return doc_titles, doc_authors


# pass in topic_docs.
# This gets you the topic assigments and strength per document.
def read_doctopics(filename):
    """ Filename input is the TopicsInDocs.csv file path."""
    docs = {}
    with open(filename, "rb") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for index, row in enumerate(spamreader):
            if index > 0:  # skip first row
                #print "row", row
                docid = row[0]
                topics = row[2:]
                topics_dict = dict(zip(topics[::2],topics[1::2]))
                #print docid, topics_dict
                docs[docid] = topics_dict
    return docs

# Make a simple csv format we could see in Excel: doc #, topic, strength, title
def doc_topics_for_excel(docs_alltopics, doc_ids, doc_authors, filename):
    ''' Produce a csv of docs, topics, scores, and filename.
    Args:
        docs_alltopics: the output from read_doctopics
        doc_ids: document ids to filename dict
        filename: to save to
    Output:
        A file we can open in excel
    '''
    with open(filename, "w") as handle:
        #print "DocID,Topic,Score,File,Author"
        handle.write("DocID,Topic,Score,File,Author\n")  # the header of the file
        for id, topics in docs_alltopics.iteritems():
            #print x, docs_alltopics[x].keys()
            for topic, score in topics.iteritems():
                #print topic, score
                #print ','.join([str(id), "Topic"+str(topic), str(score), doc_ids[id], doc_authors[id]])
                handle.write(','.join([str(id), "Topic"+str(topic), str(score), doc_ids[id], doc_authors[id] + "\n"]))

# utility function for capturing output below and writing it to a file
def writeout(string, fname):
    with open(fname, 'w') as f:
        f.write(string)

def get_doctext_for_ids(filename, NChars=200):
    """
    Pass in the Docs in Topics csv file.
    Remember that you can't ask for more NChars than you saved into the documents dict!
    """
    doc_text = {}  # dictionary, the keys will be the doc id, the filename the value
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for index, row in enumerate(spamreader):
            #print row
            if index > 0:  # skip first row making the data structure
                id = row[2]
                filename = row[3]
                with open(filename, "r") as myfile:
                    head = myfile.read(NChars).strip()
                    head = head.replace('\r', ' ')
                    doc_text[id] = head.rstrip()
    return doc_text


def remove_commas(instring):
    """ Because gephi reads in csv, you can't have commas in titles or text"""
    newstr = instring.strip()
    newstr = newstr.replace(",", "") # gephi gdf is sensitive to commas!
    newstr = newstr.replace("\n", " ")
    newstr = newstr.replace("\r", " ")
    return newstr


def writegdfnodes(word_list, docs_alltopics, doc_ids, doc_authors, documents):
    """ Creates a gephi gdf format list of nodes, from docs and topics.
        We're only writing out the top 2 words per topic node.
        Output is 2 items - a string of nodes text, and a lookup dict for the topic node number
    """
    lookup_topic = {}
    output = ""
    output += "nodedef>name VARCHAR, label VARCHAR, author VARCHAR, type VARCHAR, text VARCHAR"
    #print output
    output += "\n"

    item = 1
    for docid, doc in docs_alltopics.iteritems():
        thisline = ','.join([str(docid), doc_ids[docid], doc_authors[docid], "Doc",
                             "\"" + remove_commas(documents[docid]) + "...\""])
        #print "doc", thisline
        output += thisline + "\n"
        item += 1  # just a counter so we can sequentially add the topics after it
    # the nodes for the topics start being numbered after the doc numbers, using the counter item
    for topnum, topic in word_list.iteritems():
        thisline = ','.join([str(item), topnum + ":" + " ".join(word_list[topnum][0:2]), "Topic", "Topic", 
                             "\"Top words:" + " ".join(word_list[topnum]) + "\""])
        #print thisline
        lookup_topic[topnum] = item
        output += thisline + "\n"
        item += 1
    return output, lookup_topic


# input docs_alltopics - this outputs the links, and weights
def writegdfedges(docs, lookup_topic, weight_filter=0.1):
    """ Creates a gephi gdf format list of edges linking the nodes.
        The weight filter arg allows me to trim edges below a threshold.
        You can do some trimming in the Topic GUI, too, but here we have
        another level of control."""

    output = ""
    # Gephi prefers 'weight' and sigma.js prefers 'size' for the edge thickness, so write both
    output += "edgedef>node1 VARCHAR, node2 VARCHAR, weight DOUBLE, size DOUBLE"
    #print output
    output += "\n"

    for docnum, topics in docs.iteritems():  # if you haven't modified your dict, will be same order
        #print "Writing out ", docnum, topics
        for topicid, score in topics.iteritems():
            if float(score) > weight_filter:
                # I'm just bumping up the weight * 10 here
                thisline = str(docnum) + "," + str(lookup_topic[topicid]) + "," + str(float(score) * 10.0) + "," + str(float(score) * 10.0)
                #print thisline
                output += thisline + "\n"
    return output

def writegdf(word_list, docs_alltopics, doc_ids, doc_authors,
    documents, filename, weight_filter=0.1):
    nodestxt, lookup_topic = writegdfnodes(word_list, docs_alltopics, doc_ids, doc_authors, documents)
    edgetxt = writegdfedges(docs_alltopics, lookup_topic, weight_filter=weight_filter)
    filestring = nodestxt + edgetxt
    writeout(filestring, filename)

def main():
    # Customize these settings for your wishes and paths...
    args = len(sys.argv)
    print args

    if args < 2:
        GUI_DIR = 'topic_output/output_csv'
    else:
        GUI_DIR = sys.argv[1]
    if args < 3:
        LABEL = ''
    else:
        LABEL = sys.argv[2]

    topicWords = GUI_DIR + '/Topics_Words.csv'
    topicDocs = GUI_DIR + '/TopicsInDocs.csv'
    docTopics = GUI_DIR + '/DocsInTopics.csv'
    FILES_DIR = ''
    DocStringChars = 500
    filter_out_lower_than = 0.1

    word_list = list_words_for_topics(topicWords)
    topicCount = len(word_list)  # you will have as many as topics you requested - so, 15.
    print "Topics found in data files:", topicCount

    doc_ids, doc_authors = get_names_for_ids(docTopics)
    doc_sample = get_doctext_for_ids(docTopics, NChars=DocStringChars)

    docs_alltopics = read_doctopics(topicDocs)
    print "Documents found in data files:", len(docs_alltopics)

    file_for_excel = FILES_DIR + 'for_excel_' + LABEL + '.csv'

    doc_topics_for_excel(docs_alltopics, doc_ids, doc_authors, file_for_excel)
    print "Printed out docs and topics as csv:", file_for_excel

    filename_for_gephi = FILES_DIR + 'forgephi_topics_' + LABEL + '.gdf'
    writegdf(word_list, docs_alltopics, doc_ids, doc_authors, doc_sample,
        filename_for_gephi, weight_filter=filter_out_lower_than)
    print "Wrote out gdf file for use in gephi:", filename_for_gephi

if __name__ == "__main__":
    main()
