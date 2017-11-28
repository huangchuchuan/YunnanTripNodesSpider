# 蝉游记路线爬虫
## 运行爬虫
在`YunnanSpider`下面的目录下，修改`spiders`文件夹下面的`.py`文件中的`search_keyword`
来进行不同地方的搜索

```
# 和YunnanSpider文件夹同级目录下执行
scrapy crawl yunnan_spider -o data.json
scrapy crawl yunnan_hotplaces_spider -o goodplaces.json
```
*由于scrapy输出的json格式使用的是追加模式，所以需要先把原来的文件删除*

## 运行分析程序
把`YunnanSpider`中的`data.json`放到同级目录下
```
# 需要data.json
python generate_map_info.py
# 需要goodplaces.json
python generate_scores_file.py
# 需要data.json
python plot_network.py
```
输出为，`all_place.txt` `good_places.txt`  `map.html`  `topo/index.html`

