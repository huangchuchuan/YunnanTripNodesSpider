# -*- coding: utf-8 -*-

import json
import os
from collections import defaultdict
import traceback
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def plot_ntework_image_from_file(json_file, min_path=100):
    if not os.path.exists(json_file):
        print 'No such file: %s' % json_file
        return
    try:
        items = json.load(open(json_file))  # [{place_position, place_star, place_name, youji_url}]

        place_list = []  # 地名(正式描述)列表(只含有地图标记)
        place_name_list = []  # 地名(非正式描述)列表（所有）
        place_position_dict = {}  # 地名(正式描述)->地名(格式化描述:点，市)
        # 遍历获得地名的信息
        for item in items:
            name_list = item['place_name']
            place_name_list.extend(name_list)
            position_list = item['place_position']  # {lat:xxx, lng:xxx, description:xxx, title: xxx}
            for position_dict in position_list:
                place_list.append(position_dict['title'])
                desc = position_dict['description']
                desc = desc[1:]  # 去掉第一个<
                ps = desc.find('>') + 1  # 开始位置
                pe = desc.find('<')  # 结束位置
                desc = desc[ps: pe]
                place_position_dict[position_dict['title']] = desc
        # 构建地名(正式描述)的集合
        place_set = set(place_list)
        all_place_set = set(place_list)
        # 统计地名(正式描述)的热度 - 热度根据路线交叉数确定
        place_hot_dict = {}
        tmp_place_list = []
        # 获取中位数
        tmp = map(lambda place: place_name_list.count(place), place_set)
        min_path = min(min_path, (max(tmp) + min(tmp)) / 2)
        for place in place_set:
            n = place_name_list.count(place)
            place_hot_dict[place] = n
            if n > min_path:
                tmp_place_list.append(place)
        place_set = set(tmp_place_list)
        # 构建地名(正式描述)-id的字典
        place_id = {}
        pid = 0
        for place in place_set:
            place_id[place] = pid
            pid += 1

        # 构建place-star_list的字典
        place_star_list = defaultdict(list)
        all_place_star_list = defaultdict(list)  # 记录评分高的所有地点
        for item in items:
            l = len(item['place_star'])
            for i in range(l):
                place = item['place_name'][i]
                if place in place_set:
                    place_star_list[place].append(item['place_star'][i])
                # 记录所有的评分
                if place in all_place_set:
                    all_place_star_list[place].append(item['place_star'][i])
        # 构建place_star字典
        place_star = {}
        for name, star_list in place_star_list.iteritems():
            new_star_list = filter(lambda x: x > 1, star_list)  # 去掉1分的评分
            if len(new_star_list):
                place_star[name] = sum(new_star_list) / float(len(new_star_list))  # 对高分进行平均
            else:
                place_star[name] = 1.0  # 如果全是低分则认为只有1分
        # 构建all_place_star_list字典
        all_place_star = {}
        all_place_hot = {}
        for name, star_list in all_place_star_list.iteritems():
            all_place_hot[name] = len(star_list)
            new_star_list = filter(lambda x: x > 1, star_list)  # 去掉1分的评分
            if len(new_star_list):
                all_place_star[name] = sum(new_star_list) / float(len(new_star_list))  # 对高分进行平均
            else:
                all_place_star[name] = 1.0  # 如果全是低分则认为只有1分
        # 输出所有地点评分和热度
        file_name = 'all_places.txt'
        all_place_dict = sorted(all_place_star.iteritems(), key=lambda d: d[1], reverse=True)
        with codecs.open(file_name, 'w', 'utf-8') as f:
            for place, star in all_place_dict:
                f.write(('%s %.2f %d' + os.linesep) % (place_position_dict[place], star, all_place_hot[place]))
        # 输出好评地点
        file_name = 'good_places.txt'
        good_place_dict = sorted(place_star.iteritems(), key=lambda d: d[1], reverse=True)
        with codecs.open(file_name, 'w', 'utf-8') as f:
            for place, star in good_place_dict:
                f.write(('%s %.2f' + os.linesep) % (place_position_dict[place], star))
        # 输出热门地点
        file_name = 'hot_places.txt'
        hot_place_dict = sorted(place_hot_dict.iteritems(), key=lambda d: d[1], reverse=True)
        with codecs.open(file_name, 'w', 'utf-8') as f:
            for place, star in hot_place_dict:
                f.write(('%s %.2f' + os.linesep) % (place_position_dict[place], star))
        # 构建图数据
        print len(place_id)
        nodeDataArray = []  # 记录节点 - [{key: id, text: 地名(格式化描述:点，市)}]
        for place, id in place_id.iteritems():
            nodeDataArray.append({'key': id, 'text': place_position_dict[place]})
        linkDataArray = []  # 记录{from, to}
        linkTupleList = []  # 记录（from_id, to_id）防止添加重复的线
        linkdata = []  # 记录路线 - [地名(格式化描述:点，市)->地名(格式化描述:点，市)]
        for item in items:
            place_list = item['place_name']
            place_list = filter(lambda x: x is not None, place_list)
            place_items = []
            last_id = None
            for place in place_list:
                if place in place_id:
                    place_items.append(place_position_dict[place])
                if last_id is None:
                    if place in place_id:
                        last_id = place_id[place]
                else:
                    if place in place_id:
                        if (last_id, place_id[place]) not in linkTupleList:
                            linkTupleList.append((last_id, place_id[place]))
                            linkDataArray.append({'from': last_id, 'to': place_id[place]})
                        last_id = place_id[place]
            linkdata.append(' -> '.join(place_items))
        print len(linkTupleList)
        # 转换成字符串
        nodeDataArrayStr = json.dumps(nodeDataArray)
        linkDataArrayStr = json.dumps(linkDataArray)
        linkDataStr = json.dumps(linkdata)

        # 格式化成js代码
        nodeDataArrayStr = nodeDataArrayStr.replace('"key"', 'key').replace('"text"', 'text')
        linkDataArrayStr = linkDataArrayStr.replace('"from"', 'from').replace('"to"', 'to')
        # 生成新的html
        with open(os.path.join('topo', 'index_template.html')) as f:
            html_content = f.read()
            html_content = html_content.replace('$NODEDATAARRAY$', nodeDataArrayStr).replace('$LINKDATAARRAY$',
                                                                                             linkDataArrayStr).replace(
                '$LINKDATA$', linkDataStr)
            with codecs.open(os.path.join('topo', 'index.html'), 'w', 'utf-8') as cf:
                cf.write(html_content)

    except:
        traceback.print_exc()


if __name__ == '__main__':
    plot_ntework_image_from_file('data.json')
    pass
