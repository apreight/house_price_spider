# 基于scrapy的南京房价爬虫

### 爬取 安居客 南京历史房价 数据

_2019.03.21_ <br>
`发现一个问题`<br>
例如 `https://www.anjuke.com/fangjia/nanjing2012/`<br>
当点击到子目录 如 江宁 百家湖 时, 再 点击 全部, 有一定几率 会出现一个全国的ul列表<br>
当前解决方案:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;验证链接中是否包含 `'nanjing'`

_2019.03.22_ <br>
`存储时将地区信息与其他信息分成两个collection 降低了冗余度`