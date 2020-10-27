# Current status

current version: 0.3.2

# Changelog

## v0.3 (2020-10-27)

- 新增: 支持 Markdown 直接转换为单文件 html
- 新增: enaml 客户端支持输入 .md 文件
- 移除: enaml 客户端移除进度条

## v0.2 (2020-10-26)

- 新增: 基于 enaml 的可视化界面
- 更新: README 中对文件体积的描述
- 新增: README 添加插图
- 新增: enaml 客户端进度条
- 新增: 当转换成功时, 显示 "打开文件" 按钮

## v0.1 (2020-10-26)

- 新增: 'src/markdown_base64.py'
- 新增: 'src/html_base64.py'
- 更新: 项目数据脱敏
- 更新: 完善项目结构
- 新增: requirements.txt
- 更新: 确认 gif 图片正常显示
- 修复: 从浏览器下载 gif 到本地时的后缀名问题
- 更新: 图片后缀名从图片源文件获取
- 优化: 将共同函数移到 'src/common.py'
- 优化: 统一 'src/markdown_base64.py' 和 'src/html_base64.py' 形式
- 移除: 移除 lk-utils 依赖
