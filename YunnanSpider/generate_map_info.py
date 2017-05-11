# -*- coding: utf-8 -*-

import json
import os
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def generate_map_info(input_fils_name='data.json', output_file_name='mapinfo.csv'):
    json_data = json.load(open(input_fils_name))
    place_lat_lng_dict = {}
    for item in json_data:
        mapinfo_list = item['place_position']
        for map_dict in mapinfo_list:
            desc = map_dict['description']
            desc = desc[1:]  # 去掉第一个<
            ps = desc.find('>') + 1  # 开始位置
            pe = desc.find('<')  # 结束位置
            place = desc[ps: pe]
            positon = (map_dict['lat'], map_dict['lng'])
            place_lat_lng_dict[place] = positon
            # write file
    with codecs.open(output_file_name, 'w', 'utf-8') as f:
        for place, position in place_lat_lng_dict.iteritems():
            f.write(('%s %s %s' + os.linesep) % (place, position[0], position[1]))


def generate_map_html(input_fils_name='data.json', output_file_name='map.html'):
    marker_list = []
    json_data = json.load(open(input_fils_name))
    for item in json_data:
        marker_list.extend(item['place_position'])
    mapinfo = json.dumps(marker_list)
    with open('map_template.html') as f:
        html_content = f.read()
        html_content = html_content.replace('$MAPINFO$', mapinfo)
        with codecs.open(output_file_name, 'w', 'utf-8') as cf:
            cf.write(html_content)

if __name__ == '__main__':
    # generate_map_info()
    generate_map_html()
