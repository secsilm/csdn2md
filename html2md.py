
from bs4 import BeautifulSoup


def html_to_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    md = []

    for elem in soup.body.descendants if soup.body else soup.descendants:

        # 段落
        if elem.name == "p":
            text = elem.get_text(strip=True)
            if text:
                md.append(text)
                md.append("")

        # 代码块
        elif elem.name == "pre":
            code = elem.get_text().rstrip()
            md.append("```bash")
            md.append(code)
            md.append("```")
            md.append("")

        # 图片
        elif elem.name == "img":
            src = elem.get("src", "")
            md.append(f"![]({src})")
            md.append("")

        # 链接（单独成段的情况）
        elif elem.name == "a":
            href = elem.get("href", "")
            text = elem.get_text(strip=True)
            if href:
                md.append(f"[{text}]({href})")
                md.append("")

    return "\n".join(md).strip()


if __name__ == "__main__":

    html_content = """
<h1>1.麦克风无法正常输入输出以及VoodooHDA启动慢 解决方法</h1>\n\n<p>很简单，参考了 这个人的做法</p>\n\n<p><a href=\"https://github.com/athlonreg/AppleALC-ALCPlugFix\">https://github.com/athlonreg/AppleALC-ALCPlugFix</a></p>\n\n<p>去/System/Library/Extensions 里面把AppleHDA删除即可，同时在EFI的clover/kexts/里安装VoodooHDA即可，主要原因是苹果本身的声卡驱动AppleHDA和VoodooHDA万能声卡驱动的冲突问题。</p>\n\n<p>If your headphone and microphone don't work normally in hackintosh, just install the universe audio driver named VoodooHDA.</p>\n\n<p>and to solve the problem about the hackintosh longtime boot loading after installed VoodooHDA, Just to remove the AppleHDA.kexts in/System/Library/Extensions . because of the reason that these two have conflicts.</p>\n\n<p>另外，由于我的主板有一个特点，就是电脑长期不用会进入休眠状态，必须重新按电源以唤醒，然而我的黑苹果在被唤醒以后，声音无法正常输出，因此考虑到是声音驱动的问题，尝试重新卸载驱动</p>\n\n<pre class=\"has\">\n<code class=\"language-bash\">sudo kextunload /System/Library/Extensions/VoodooHDA.kext\n</code></pre>\n\n<p>如果报错，多卸载几次就会成功，然而卸载之后装回去就需要用到命令</p>\n\n<pre class=\"has\">\n<code>sudo kextload /System/Library/Extensions/VoodooHDA.kext\n</code></pre>\n\n<p>这步报错了，提示</p>\n\n<pre class=\"has\">\n<code>/System/Library/Extensions/VoodooHDA.kext failed to load - (libkern/kext) authentication failure \n(file ownership/permissions); check the system/kernel logs for errors or try kextutil(8).</code></pre>\n\n<p> </p>\n\n<p>意思是权限问题，于是我又加了权限</p>\n\n<pre class=\"has\">\n<code>sudo chmod -R 777 /System/Library/Extensions/VoodooHDA.kext\n</code></pre>\n\n<p>但是依旧报错，依据报错内容，我试图查看system/kernel的log，但是找了一圈找不到内核日志在哪，于是就依据kextutil(8)的提示使用了如下命令</p>\n\n<pre class=\"has\">\n<code>sudo kextutil /System/Library/Extensions/VoodooHDA.kext\n</code></pre>\n\n<p>提示如下信息 </p>\n\n<pre class=\"has\">\n<code>Kext with invalid signatured (-67062) allowed: &lt;OSKext 0x7fb4c1e0c980 [0x7fff8b341b30]&gt; { URL =\n \"file:///Library/Extensions/VoodooHDA.kext/\", ID = \"org.voodoo.driver.VoodooHDA\" }\nKext rejected due to improper filesystem permissions: &lt;OSKext 0x7fb4c1e07ff0 [0x7fff8b341b30]&gt; { URL = \n\"file:///System/Library/Extensions/VoodooHDA.kext/\", ID = \"org.voodoo.driver.VoodooHDA\" }\nCode Signing Failure: not code signed\nAuthentication Failures: \n    File owner/permissions are incorrect (must be root:wheel, nonwritable by group/other): \n        /System/Library/Extensions/VoodooHDA.kext\n        Contents\n        Info.plist\n        MacOS\n        VoodooHDA\n\nDiagnostics for /System/Library/Extensions/VoodooHDA.kext:\nAuthentication Failures: \n    File owner/permissions are incorrect (must be root:wheel, nonwritable by group/other): \n        /System/Library/Extensions/VoodooHDA.kext\n        Contents\n        Info.plist\n        MacOS\n        VoodooHDA\n</code></pre>\n\n<p>可见，权限设置必须为“must be root:wheel, nonwritable by group/other”，真是大开眼界，看来权限不是越大越好，这里会检测用户组的权限，如果有写权限就会报错。于是，我修改权限之后成功load恢复声音驱动。</p>\n\n<pre class=\"has\">\n<code>sudo chmod -R 755 /System/Library/Extensions/VoodooHDA.kext\n\nsudo chown -R root /System/Library/Extensions/VoodooHDA.kext\n\nsudo chgrp -R wheel /System/Library/Extensions/VoodooHDA.kext\n\nsudo kextload /System/Library/Extensions/VoodooHDA.kext</code></pre>\n\n<p>终于又有声音了！</p>\n\n<h1>2.VoodooHDA设置无法保存的解决方法</h1>\n\n<p>首先去这里下载voodoohda的最新版本：</p>\n\n<p><a href=\"https://github.com/chris1111/VoodooHDA-2.9.2-Clover-V14/releases\">https://github.com/chris1111/VoodooHDA-2.9.2-Clover-V14/releases</a></p>\n\n<p><img alt=\"\" class=\"has\" height=\"442\" src=\"https://i-blog.csdnimg.cn/blog_migrate/f9b841c1c95bc42882ce5d0c51673833.png\" width=\"624\" /></p>\n\n<p>下载完之后会提示你安装，在这里选择自定</p>\n\n<p><img alt=\"\" class=\"has\" height=\"434\" src=\"https://i-blog.csdnimg.cn/blog_migrate/8b6949bcf54aa2c7b3e6aeb6690ab760.png\" width=\"608\" /></p>\n\n<p>选择你需要的版本，比如我是mojave</p>\n\n<p><img alt=\"\" class=\"has\" height=\"438\" src=\"https://i-blog.csdnimg.cn/blog_migrate/ba67d2aaf71add991c611c8569ceb67c.png\" width=\"626\" /></p>\n\n<p>之后安装完之后去系统偏好设置-&gt;用户与群组-&gt;登录项</p>\n\n<p>里面把voodoohda选上</p>\n\n<p><img alt=\"\" class=\"has\" height=\"456\" src=\"https://i-blog.csdnimg.cn/blog_migrate/5f429e9630816a17ceaa6464558a215f.png\" width=\"796\" /></p>\n\n<p> </p>\n\n<p><img alt=\"\" class=\"has\" height=\"486\" src=\"https://i-blog.csdnimg.cn/blog_migrate/27e852121ef88a5c9beb209c1b6c8670.png\" width=\"674\" /></p>\n\n<p>之后就能够在偏好里保存设置了。</p>\n\n<p><img alt=\"\" class=\"has\" height=\"597\" src=\"https://i-blog.csdnimg.cn/blog_migrate/e4848379e711a9b81420c16ddccdc5da.png\" width=\"689\" /></p>\n\n<p><img alt=\"\" class=\"has\" height=\"554\" src=\"https://i-blog.csdnimg.cn/blog_migrate/9558e8760e3dd55a2478ec215508f553.png\" width=\"676\" /></p>\n,
    """
    markdown = html_to_markdown(html_content)

    with open("output.md", "w", encoding="utf-8") as f:
        f.write(markdown)

    print("转换完成：output.md")
