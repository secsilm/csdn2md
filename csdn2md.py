# coding: utf-8
"""一个用于将 csdn 博客导出为 markdown 文件的程序。

为了将自己的 csdn 博客文件导出放到我的 [hexo 站点](https://secsilm.github.io/)上，
我写了这个程序来导出文件，并加上 hexo 所需要的头部说明（title、date 等等）。

我收集了很多 UA 放在 uas.txt 文件中，当然这个程序用不到那么多。

你需要先在网页上登录自己的 csdn 博客，然后把 cookies 复制到 cookies.txt 文件里。

需要注意的是如果你当初写博客的时候不是用 markdown 编辑器写的，那么这个程序是不支持的。

Good luck，CSDN sucks。
"""
import hmac
import json
import logging
import os
import uuid
import fire
import requests
import base64
import hashlib
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
# CSDN 固定的签名常量，抓包得到
APP_KEY = ""
APP_SECRET = ""

def get_csdn_headers(method, url, params=None):
    """
    根据源代码逻辑生成动态签名 Headers
    """
    x_ca_nonce = str(uuid.uuid4())
    accept = "*/*"
    content_type = "application/json;charset=UTF-8"
    date = ""
    
    # 1. 提取路径并对参数排序
    # 只保留路径部分，剔除域名
    path = url.replace("https://bizapi.csdn.net", "")
    
    if params:
        # 按 Key 字典序排序
        sorted_keys = sorted(params.keys())
        query_str = "&".join([f"{k}={params[k]}" for k in sorted_keys])
        path_with_params = f"{path}?{query_str}"
    else:
        path_with_params = path

    # 2. 构造待签名字符串 (String_To_Sign)
    # 顺序：Method, Accept, Content-MD5, Content-Type, Date, Headers, Path
    # 注意 headers 部分只包含 x-ca-key 和 x-ca-nonce
    headers_to_sign = f"x-ca-key:{APP_KEY}\nx-ca-nonce:{x_ca_nonce}\n"
    
    string_to_sign = (
        f"{method.upper()}\n"
        f"{accept}\n"
        f"\n"  # Content-MD5 留空
        f"{content_type}\n"
        f"{date}\n"
        f"{headers_to_sign}"
        f"{path_with_params}"
    )

    # 3. 计算 HMAC-SHA256
    signature = base64.b64encode(
        hmac.new(
            APP_SECRET.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).digest()
    ).decode('utf-8')

    return {
        'accept': accept,
        'content-type': content_type,
        'x-ca-key': APP_KEY,
        'x-ca-nonce': x_ca_nonce,
        'x-ca-signature': signature,
        'x-ca-signature-headers': 'x-ca-key,x-ca-nonce',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://editor.csdn.net/',
        'origin': 'https://editor.csdn.net'
    }


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
    cookies = {
       #开发工具复制为py之后使用curl2python生成
    }

            

    for p in range(start, stop + 1):
        logging.info('Page {}'.format(p))
        # 获取该页文章
        headers = {

        'accept': '*/*',

        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',

        'cache-control': 'no-cache',

        'origin': 'https://editor.csdn.net',

        'pragma': 'no-cache',

        'priority': 'u=1, i',

        'referer': 'https://editor.csdn.net/',

        'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',

        'sec-ch-ua-mobile': '?0',

        'sec-ch-ua-platform': '"Windows"',

        'sec-fetch-dest': 'empty',

        'sec-fetch-mode': 'cors',

        'sec-fetch-site': 'same-site',

        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',

    }
        response=requests.get(
            'https://blog.csdn.net/'+username+'/article/list/' + str(p), cookies=cookies,headers=headers)
        articles = response.text
        soup = BeautifulSoup(articles, 'lxml')
        for article in soup.find_all('div', attrs={'class':'article-item-box'}):
            print(article)
            article_id = article['data-articleid']
            create = article.find('span',attrs={'class':'date'}).text
            base_url = 'https://bizapi.csdn.net/blog-console-api/v3/editor/getArticle'
            params = {
                'id': article_id
            }
            print(article_id)
            # 根据文章 id 获取文章数据
                # 关键：动态获取 Headers
            headers = get_csdn_headers("GET", base_url, params)
            r = requests.get(base_url, params=params, cookies=cookies,headers=headers)
            try:
                data = json.loads(r.text, strict=False)
#                print(data)
            except Exception as e:
                logging.error('Something wrong happend. {}'.format(e))
            # 标题
            print(data)
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
                hexo_str = '---\ntitle: "{title}"\ndate: {date}\ntags:\n---\n\n'.format(
                    title=title, date=create)
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
