# coding: utf-8
"""一个用于将 csdn 博客导出为 markdown 文件的程序。

为了将自己的 csdn 博客文件导出放到我的 [hexo 站点](https://secsilm.github.io/)上，
我写了这个程序来导出文件，并加上 hexo 所需要的头部说明（title、date 等等）。

我收集了很多 UA 放在 uas.txt 文件中，当然这个程序用不到那么多。

你需要先在网页上登录自己的 csdn 博客，然后把 cookies 复制到 cookies.txt 文件里。

需要注意的是如果你当初写博客的时候不是用 markdown 编辑器写的，那么这个程序是不支持的。

Good luck，CSDN sucks。
"""

import json
import logging
import os

import fire
import requests
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


def read_and_parse_cookies(cookie_file):
    """读取并解析 cookies。

    Args:
        cookie_file: 含有 cookies 字符串的 txt 文件名

    Returns:
        一个字典形式的 cookies
    """
    with open(cookie_file, 'r') as f:
        cookies_str = f.readline()
    cookies_dict = {}
    for item in cookies_str.split(";"):
        k, v = item.split("=", maxsplit=1)
        cookies_dict[k.strip()] = v.strip()
    return cookies_dict


def to_md_files(username, total_pages, cookie_file, start=1, stop=None, hexo=True, md_dir='.'):
    """导出为 Markdown 文件。

    Args:
        total_pages: 博客文章在摘要模式下的总页数
        filename: 含有 cookies 字符串的 txt 文件名
        start: 从 start 页开始导出 (default: {1})
        stop: 到 stop 页停止 (default: {None})
        hexo: 是否添加 hexo 文章头部字符串（default: {True}）
        md_dir: md 文件导出目录，默认为当前目录（default: .）
    """
    if stop is None:
        stop = total_pages
    if not os.path.exists(md_dir):
        os.makedirs(md_dir)
    # 全部可用的 UA 在 usa.txt 文件中
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
    }
    cookies = read_and_parse_cookies(cookie_file)
    for p in range(start, stop + 1):
        logging.info('Page {}'.format(p))
        # 获取该页文章
        articles = requests.get(
            'http://blog.csdn.net/u010099080/article/list/' + str(p), cookies=cookies).text
        soup = BeautifulSoup(articles, 'lxml')
        for article in soup.find('div', id='article_list').find_all('a', href=True, title=False):
            article_id = article['href'].split('/')[-1]
            base_url = 'http://write.blog.csdn.net/mdeditor/getArticle'
            params = {
                'id': article_id,
                'username': username
            }
            # 根据文章 id 获取文章数据
            r = requests.get(base_url, params=params, cookies=cookies)
            try:
                data = json.loads(r.text, strict=False)
            except Exception as e:
                logging.error('Something wrong happend. {}'.format(e))
            # 标题
            title = data['data']['title'].strip()
            # md 形式的文章内容
            content = data['data']['markdowncontent']
            if content is None:
                logging.error(
                    '{title} is not written with markdown.'.format(title))
                continue
            logging.info('Exporting {} ...'.format(title))
            # hexo_str 是用 hexo 写文章时需要在头部加的东西
            hexo_str = ''
            if hexo:
                hexo_str = '---\ntitle: {title}\ndate: {date}\ntags:\n---\n\n'.format(
                    title=title, date=data['data']['create'])
            # Windows 下文件名中的非法字符
            forbidden = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
            # 如果文章名含有非法字符，那么使用其 id 作为 md 文件名
            if any([c in repr(title) for c in forbidden]):
                with open(os.path.join(md_dir, article_id + '.md'), 'w', encoding='utf8') as f:
                    f.write(hexo_str + data['data']['markdowncontent'])
            else:
                with open(os.path.join(md_dir, title + '.md'), 'w', encoding='utf8') as f:
                    f.write(hexo_str + data['data']['markdowncontent'])
    logging.info('Done!')


if __name__ == '__main__':
    fire.Fire(to_md_files)
