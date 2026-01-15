# csdn2md

Export csdn blogs to markdown files.

一个用于将 csdn 博客导出为 markdown 文件的程序。

为了将自己的 csdn 博客文件导出放到我的 [hexo 站点](https://secsilm.github.io/)上，
我写了这个程序来导出文件，并加上 hexo 所需要的头部说明（title、date 等等）。

我收集了很多 UA 放在 `uas.txt` 文件中，当然这个程序用不到那么多。

你需要先在网页上登录自己的 csdn 博客，然后把 cookies 复制到 `cookies.txt` 文件里。

需要注意的是如果你当初写博客的时候不是用 markdown 编辑器写的，那么这个程序是不支持的。

Good luck，CSDN sucks。
脚本说明：
```bash
python .\csdn2md.py fjh1997 11  cookies.txt #表示用户名和页数还有cookie文件（cookie文件没用）
python picConvert.py #用于转换当前目录md里面的图片到github仓库里面，需要填下github token
python html2md.py #用于转换富文本编辑格式的博文为markdown，里面的内容需要自己通过https://bizapi.csdn.net/blog-console-api/v1/editor/getArticle?id=85729073
接口获取

```
github token可以去这里获取https://github.com/settings/tokens
里面这样选：
<img width="1133" height="887" alt="image" src="https://github.com/user-attachments/assets/2423d58a-5fc5-4501-b137-fe541698b646" />
