# 项目说明

我们平时将 markdown 格式导出为 html, 再将 html 另存为 mhtml 格式, 会发现原先 html 中引用的本地图片, 在 mhtml 中丢失了.

[这篇文章](https://blog.csdn.net/ybf326/article/details/84781746) 介绍了一种解决方法, 但是操作难度高, 不太实用.

本项目为解决此问题提供了更好的方案: 通过程序将 markdown 或 markdown 导出的 html 中引用的本地图片转换为 base64 格式, 并替换到原文中.

简而言之, 本项目的最终目的是, 将 markdown 及其插图 **以单个 html 文件完整呈现**.

演示用例 1:

1. 准备一个 markdown 文件: "examples/demo.md"

2. 运行 'src/launch_gui.py', 弹出可视化界面

   ![image-20201026153247849](.assets/image-20201026153247849.png)

3. 输入或选择 .md 文件, 点击 "Run" 按钮

4. 提示生成成功, 生成文件在 "examples/demo_base64.html"

   ![image-20201026153418122](.assets/image-20201026153418122.png)

注意:

1. 目前仅支持对本地图片的获取和编码

# 开发者说明

## 生成文件的体积对比

以演示用例为例, 'examples/demo.html' 大小约 18kb, 该 html 引用了两张图片的大小分别为 19kb 和 33kb.

使用浏览器的 "转换为 mhtml" 功能, 生成的 .mhtml 文件的大小为 90kb; 使用 'src/html_base64.py' 生成的 'examples/demo_base64.html' 文件的大小为 86kb.

![image-20201026152235057](.assets/image-20201026152235057.png)

结论:

1. 本程序生成的 base64 编码的 html 体积上比浏览器生成的 .mhtml 略小一些

2. base64 编码的 html 比原 html + 原图片的体积略大, 这是因为 base64 编码的原因 (base64 编码的图片会比原图大 1/3)

## 项目依赖须知

enaml 模块在 Python 3.9 中启动会报错 (相关见 [这个讨论](https://docs.python.org/3/whatsnew/3.8.html#cpython-bytecode-changes)), 请使用 Python 3.8 或以下版本.
