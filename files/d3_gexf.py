
"""
Usage: >python d3_gexf.py csvfile label  OR
OR: >python d3_gexf.py csvfile label csvfile2 label2

Requires you to have pandas, numpy, and networkx installed.
>pip install pandas (it will install numpy too)
>pip install networkx

@arnicas (Aug 2014)
"""


import json
from networkx.readwrite import json_graph
import pandas as pd
import networkx as nx  # http://networkx.github.io/documentation/networkx-1.9/index.html
import numpy as np
import sys


# make a list of edges - with a weight for each pair found.
def make_edges_dict(df):
    from collections import defaultdict
    edges = defaultdict(list)
    import itertools
    for num in range(1,16):
        docIDs = df[df["Topic"]=="Topic" + str(num)]['DocID']
        scores = df[df["Topic"]=="Topic" + str(num)]['Score']
        pairs = zip(docIDs,scores)
        combos = [x for x in itertools.combinations(pairs,2)]
        for pair in combos:
            #print pair
            node1 = pair[0][0]
            node2 = pair[1][0]
            weight1 = pair[0][1]
            weight2 = pair[1][1]
            if weight1 and weight2:
                if weight1 != weight2:
                    weight = (1 / abs(pair[0][1] - pair[1][1])) / 10
                else:
                    weight = 100
                if node2 < node1:
                    node1, node2 = node2, node1
                edges[(node1,node2)].append(weight)
    return edges

def write_gexf_from_csv(excelcsv, outputfile, edgelabel = 'allwords'):
    df = pd.read_csv(excelcsv)
    edges = make_edges_dict(df)
    g = nx.Graph()
    for pair, weight in edges.iteritems():  # if you haven't modified your dict, will be same order
        g.add_edge(pair[0],pair[1], weight=float(np.mean(weight)), score=float(np.mean(weight)), 
                   count=len(weight), median=float(np.median(weight)), label=edgelabel)
    df_files = df[['DocID','Author','File']].drop_duplicates()
    for index, row in df_files.iterrows():
        g.add_node(row['DocID'], author = row['Author'], label = row['File'])
    nx.write_gexf(g, outputfile)
    print "Wrote ", outputfile
    return g

def add_edges_to_first(g, edge_dir):
    for pair, weight in edge_dir.iteritems():  # if you haven't modified your dict, will be same order
        g.add_edge(pair[0],pair[1], weight=float(np.mean(weight)), score=float(np.mean(weight)), 
            count=len(weight), median=float(np.median(weight)), label="verbs") 
    return g

def write_jsonfile(g, outputfile):
    g_json = json_graph.node_link_data(g) # node-link format to serialize
    json.dump(g_json, open(outputfile,'w'))
    print "Wrote ", outputfile

def main():
    print len(sys.argv)

    if len(sys.argv) < 3:
        print 'Usage: '
        print 'd3_gexf.py [pivot_csv] [label] or '
        print 'd3_gexf.py [pivot_csv1] [label1] [pivot_csv2] [label2]'
        sys.exit()
    if len(sys.argv) >= 3:
        csv1 = sys.argv[1]
        label1 = sys.argv[2]
        output1 = 'gexf_' + label1 + '.gexf'
        output1json = 'network_' + label1 + '.json'
        g1 = write_gexf_from_csv(csv1, output1, edgelabel=label1)
        write_jsonfile(g1, output1json)
    if len(sys.argv) == 5:
        print 'Found a second file of input.'
        csv2 = sys.argv[3]
        label2 = sys.argv[4]
        output2 = 'gexf_' + label2 + '.gexf'
        output2json = 'network_' + label2 + '.json'
        output_combined_json = 'network_' + label1 + '_' + label2 + '.json'
        g2 = write_gexf_from_csv(csv2, output2, edgelabel=label2)
        write_jsonfile(g2, output2json)
        print "Writing a combined json file, too:"
        df_new = pd.read_csv(csv2)
        edges_new = make_edges_dict(df_new)
        g = add_edges_to_first(g1, edges_new)
        write_jsonfile(g, output_combined_json)

if __name__ == "__main__":
    main()

