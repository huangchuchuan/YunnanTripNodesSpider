# -*- coding: utf-8 -*-

import json
import os
import networkx
import matplotlib.pyplot as plt
from collections import defaultdict
import traceback
import codecs


def plot_ntework_image_from_file(json_file):
    if not os.path.exists(json_file):
        print 'No such file: %s' % json_file
        return
    try:
        items = json.load(open(json_file))
        # 构建place-star_list的字典
        place_star_list = defaultdict(list)
        for item in items:
            l = len(item['place_star'])
            for i in range(l):
                place_star_list[item['place_name'][i]].append(item['place_star'][i])
        # 构建place_star字典
        place_star = {}
        place_id = {}
        pid = 0
        for name, star_list in place_star_list.iteritems():
            new_star_list = filter(lambda x: x > 1, star_list)  # 去掉1分的评分
            if len(new_star_list):
                place_star[name] = sum(new_star_list)/float(len(new_star_list))  # 对高分进行平均
            else:
                place_star[name] = 1.0  # 如果全是低分则认为只有1分
            place_id[name] = pid
            pid += 1
        # # 构建无向图
        # G = networkx.Graph()
        # last_node = None
        # for item in items:
        #     places = item['place_name']
        #     for place in places:
        #         pid = place_id[place]
        #         if not G.has_node(pid):
        #             G.add_node(pid, time='%.2fpm'%place_star[place])
        #         if last_node is None:
        #             last_node = pid
        #         else:
        #             if not G.has_edge(last_node, pid):
        #                 G.add_edge(last_node, pid)
        #             last_node = pid
        # # 画图
        # networkx.draw(G)
        # plt.show()
        # 输出热门地点
        file_name = 'hot_places.txt'
        hot_place_dict = sorted(place_star.iteritems(), key=lambda d: d[1], reverse=True)
        with codecs.open(file_name, 'w', 'utf-8') as f:
            for place, star in hot_place_dict:
                f.write(('%s %.2f'+os.linesep) % (place, star))

    except:
        traceback.print_exc()
        print 'invalid json format data'


if __name__ == '__main__':
    plot_ntework_image_from_file('data.json')
    pass
