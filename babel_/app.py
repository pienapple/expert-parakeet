from gettext import translation
import os

root_dir = os.path.join(os.path.dirname(__file__), "i18n")

#: Babel
'''
pybabel init
  -D domain, --domain=DOMAIN   [domain of PO file (default 'messages')]
  -i input_file, --input-file=INPUT_FILE
  -d output_dir, --output-dir=OUTPUT_DIR
  -l locale, --locale=LOCALE

=> <output_dir>/<locale>/LC_MESSAGES/<domain>.po

'''

#: gettext
'''
pybabel init -d i18n -l zh -D messages -i messages.pot 
=> i18n/zh/LC_MESSAGES/messages.po
=> localedir/languages[x]/LC_MESSAGES/<domain>.po
'''

t = translation(domain="messages", localedir=root_dir, languages=["zh_CN"])
t.install(names=["ngettext", "gettext"])


# pythonic code
py_str1 = _('Hello World -py1 !')
py_str3 = gettext("""
Hello World -py3!
""")