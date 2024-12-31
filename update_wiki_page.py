import requests
import json
import os
import re
from datetime import datetime
import pytz  # 引入时区库

# ====== 文件路径设置 ======
readme_file = os.path.join("README.md")  # 主仓库根目录下的 README.md 文件

# ====== 获取当前北京时间 ======
shanghai_tz = pytz.timezone("Asia/Shanghai")
current_time = datetime.now(shanghai_tz).strftime("%Y年%m月%d日%H点%M分")

# ====== 请求接口获取数据 ======
import scrapy
from scrapy.crawler import CrawlerProcess

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://ymxfx.xyz']

    def parse(self, response):
        # 爬取首页的列表中的第一个链接
        first_link = response.css('.ect-entry-card a::attr(href)').get()
        yield response.follow(first_link, self.parse_detail)

    def parse_detail(self, response):
        # 爬取详情页面的含有"api"的网址
        pattern = r"http?://(?:[-\w]+\.)+[a-z]{2,6}(?:[-\w ./]+[!&(),=~_?\$]*)(?:subscribe(?:[^\s]*)?)"
        matches = re.findall(pattern, response.text)
        data = '\n'.join(set(match.replace('</div><div', '').replace('"', '') for match in matches))
        print(data)
        # 获取html内容的title
        title = response.css('title::text').get()
        print(title)
        # 更新域名数字，适配单个域名 167557.xyz
        updated_content = f" 免费节点分享 \n- 域名: {self.start_urls} \n- 标题:{title} \n- 内容: \n{data} \n- 更新时间: {current_time} \n结束"
        # ====== 更新 README.md 文件 ======
        if not os.path.exists(readme_file):
            raise FileNotFoundError(f"{readme_file} 不存在，请检查路径。")

        with open(readme_file, "r", encoding="utf-8") as file:
            readme_content = file.read()

        # 替换 README.md 中的更新时间
        updated_readme_content = re.sub(
            r" 免费节点分享.*结束",
            updated_content,
            readme_content,
            flags=re.DOTALL
        )

        # 写回更新内容
        with open(readme_file, "w", encoding="utf-8") as file:
            file.write(updated_readme_content)

        print(f"README.md 内容已更新：当前北京时间为 {current_time}")

# 调用爬虫

process = CrawlerProcess()
process.crawl(MySpider)
process.start()


