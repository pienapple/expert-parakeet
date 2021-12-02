from babel_.app import t
import os
from jinja2 import Environment
from jinja2 import FileSystemLoader


# babel python消息国际化
from babel_.app import py_str1, py_str3
print(py_str1, py_str3, sep='\n')


# babel html, jinja2的模板国际化
def render(template_name, context):
    tmpl = jinja_env.get_template(template_name)
    return tmpl.render(**context)


template_path = os.path.join(os.path.dirname(__file__), "babel_/templates")
jinja_env = Environment(
    loader=FileSystemLoader(template_path), autoescape=True,
    extensions=['jinja2.ext.i18n']
)


data = render("index.html", {"gettext": t.gettext})
print(data)

# 向环境动态添加扩展
jinja_env.add_extension('jinja2.ext.do')
