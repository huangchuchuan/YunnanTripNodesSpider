# -*- coding: utf-8 -*-

import json
import os
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def generate_socres_file(input_fils_name='goodplaces.json', output_file_name='scores.txt'):
    json_data = json.load(open(input_fils_name))
    name_score_dict = {}
    for item in json_data:
        scores = item['place_score']
        places = item['place_name']
        item_size = len(scores)
        for i in range(item_size):
            name_score_dict[places[i]] = scores[i]
    # sort
    name_score_list = sorted(name_score_dict.iteritems(), key=lambda d:d[1], reverse=True)
    # write file
    with codecs.open(output_file_name, 'w', 'utf-8') as f:
        for name_score in name_score_list:
            f.write(('%s %s'+os.linesep) % (name_score[0], name_score[1]))


if __name__ == '__main__':
    generate_socres_file()
