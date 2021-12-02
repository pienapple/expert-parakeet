##### 文件目录说明
gettext_example假设为一个项目根目录，包含入口app.py和子目录sub_
pygettext.py msgfmt.py 从$PYTHON_ROOT/Tools/i18n 拷贝出来, 方便运行,从根目录提取消息
运行：
> python pygettext.py gettext_example
--> 生成messages.pot -> messages.po
> python msgfmt.py messages.po
--> 生成messages.mo -> zh_CN.mo -> 拷贝到 