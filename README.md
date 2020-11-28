# 项目说明

本程序用于将 markdown 转换为单 html 文件, 并着重解决 **本地图片如何嵌入 html** 的问题.

本程序具有以下特点:

1. 使用简单, 只需传入 .md 文件, 即可一键生成 .html
2. 单文件输出. 无需考虑 markdown 中引用的本地路径的图片, 因为它们已经被嵌入在 html 文件中
3. 便于分享. 您只需要将此 html 文件发送给朋友, 对方即可看到完整的页面内容

# 安装

将本项目克隆到本地, pip 安装 requirements 中列出的依赖.

注意: 您需要使用 Python 3.8 版本. 因为依赖项 lk-logger 在 Python 3.7 及以下会报语法错误; 依赖项 enaml 在 Python 3.9 版本会报内置模块引起的错误 (相关见 [这个讨论](https://docs.python.org/3/whatsnew/3.8.html#cpython-bytecode-changes)).

# 如何使用

1. 准备一个 markdown 文件: "examples/demo.md"

2. 运行 'src/launch_gui.py', 弹出可视化界面

   ![image-20201026153247849](.assets/image-20201026153247849.png)

3. 输入或选择 .md 文件, 点击 "Run" 按钮

4. 提示生成成功, 生成文件与 markdown 文件在同一目录, 与 markdown 文件同名 (后者后缀是 ".html")

   ![image-20201026153418122](.assets/image-20201026153418122.png)

注意:

1. 目前仅支持对本地图片的获取和编码

2. 当图片较多时, 需要较长的处理时间 (大量优化待完成)

# 开发者说明

## 生成文件的体积对比

以演示用例为例, 'examples/demo.html' 大小约 18kb, 该 html 引用了两张图片的大小分别为 19kb 和 33kb.

使用浏览器的 "转换为 mhtml" 功能, 生成的 .mhtml 文件的大小为 90kb; 使用 'src/html_base64.py' 生成的 'examples/demo_base64.html' 文件的大小为 86kb.

![image-20201026152235057](.assets/image-20201026152235057.png)

结论:

1. 本程序生成的 base64 编码的 html 体积上比浏览器生成的 .mhtml 略小一些

2. base64 编码的 html 比原 html + 原图片的体积略大, 这是因为 base64 编码的原因 (base64 编码的图片会比原图大 1/3)

