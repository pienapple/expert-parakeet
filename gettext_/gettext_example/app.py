from gettext import translation
import os
import babel

root_dir = os.path.join(os.path.dirname(__file__), "i18n")

# mo文件位置 localedir/languages[x]/LC_MESSAGES/domain.mo
# -> ./i18n/zh/LC_MESSAGES/zh_CN.mo
t = translation(domain="zh_CN", localedir=root_dir, languages=["zh"])
_ = t.gettext


c_str = _("Hello World")

py_str = _('Hello World, %s') % "app"

# ntext = ngettext("Hello World 1", "Hello World 2", 1)

