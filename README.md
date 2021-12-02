### python-i18n / pythonweb国际化

​       &nbsp;&nbsp;&nbsp;&nbsp; 国际化可以方便我们以一种语言(英语)编写程序中的字符串，但是可以向不同国家的人提供对应的语言翻译，那么python语言如何实现国际化呢？ python内置模块gettext为python模块和应用提供了国际化(i18n)和本地化支持，它既支持GNU-gettext的消息翻译，又提供了更适合python基于类的程序消息翻译接口。

#### 一、 python-gettext (内置模块)

##### 1.1 gettext生成翻译

&nbsp;&nbsp;&nbsp;&nbsp; [GNU-gettext](http://www.gnu.org/software/gettext/gettext.html) 提供C代码的国际化，GNU-gettext制定了翻译文件的格式，提供一个工具集(一系列命令)来解析文件。Windows用户可以从官网下载压缩包解压，Linux用户通过**yum install xgettext**完成安装。完成国际化的一般步骤：

- (1) *gettext* - 从源程序提取消息，生成翻译文件messages.pot (以**msgid/msgstr**对组织)， 修改msgstr对应的翻译；
- (2) *msgfmt* - 将**messages.pot**编译成**messages.mo**文件(一种格式标准，现在大家都遵守)。
- (3) 程序配置时，需要指明mo文件位置，以供程序解析加载(类似字典对)。

​	&nbsp;&nbsp;&nbsp;&nbsp; **GNU-gettext**只提供C风格字符串(双引号)的识别，对于python特有的三引号和单引号那应该怎么办呢？其实我们要提取和编译也可以不用安装xgettext工具，在python安装目录下 **ROOT_PYTHON/Tools/i18n** 提供了这两个工具(没有可以在cpython源码中下载 [py-i18n-tools](https://github.com/python/cpython/blob/main/Tools/i18n))，按照GNU-gettext标准，**pygettext.py** 来扫描python源码生成**pot文件**，mgsfmt.py来编译pot文件生成**mo文件**(有兴趣的朋友可以阅读了解下mo文件生成格式)。下面我们来使用python-gettext进行一下翻译：

###### (1) 编写源代码 app.py

-  translation用来解析mo文件， 返回一个标准的GNUTranslations；
-  gettext 用于从解析后的字典里取值，没有翻译值，则保持原样；

```python
from gettext import translation
import os

root_dir = os.path.join(os.path.dirname(__file__), "i18n")

# 从 localedir/languages[x]/LC_MESSAGES/domain.mo 读取文件， localedir请传入一个绝对路径
t = translation(domain="zh_CN", localedir=root_dir, languages=["zh"])
_ = t.gettext


c_str = _("Hello World")

py_str = _('Hello World, %s') % "app"
```

###### (2) 提取源代码消息：

​	    &nbsp;&nbsp;&nbsp;&nbsp; 生成的pot文件格式头由一对空msgid/msgstr组成，其后紧跟的一堆为文件的元信息，其中Content-Type用于说明文件格式及编码，中文请改为charset=UTF-8。

~~~bash
python pygettext.py app.py
# gettext 后跟一个文件或目录， 目录则递归扫描
# -o 指定输出文件名称，无该选项则默认为messages.pot
~~~

  

 - pot文件格式 / po文件格式：

```bash

# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR ORGANIZATION
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"POT-Creation-Date: 2021-11-27 23:37+0800\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: pygettext.py 1.5\n"


#: i18n_\app.py:12
msgid "Hello World"
msgstr ""

```

###### (3) 编译pot文件：

```bash
修改messesges.pot文件的msgstr为对应中文翻译
messages.pot -> messages.po
python msgfmt.py messages.po
# -o 指定输出文件名称，无该选项则默认为 输入文件名称.mo
# 将messages.mo -> zh_CN.mo 并移动到同级目录 i18n/zh/LC_MESSAGES下
​```
注意 文件结构
app.py
|
i18n/zh/LC_MESSAGES/zh_CN.mo
|
messages.po
|
messages.mo
​```
```

##### 1.2 gettext模块详解：

mo文件位置拼接： **localedir/languages[x]/LC_MESSAGES/domain.mo**

###### (1) find函数：

- 功能说明：根据指定参数定位mo翻译文件位置
- 返回值：列表 [mo文件位置]
- 参数说明：

  | 参数             | 说明                                                         |
  | :---------------- | :------------------------------------------------------------ |
  | domain/localedir | 翻译文件名称 / 语言文件根目录                                |
  | languages        | 语言列表<br/>不提供则在环境变量找 'LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'，找不到返回空列表 |
  | all              | 是否返回全部languages的mo文件位置，默认为False， 返回第一个找到的文件 |

  

###### (2) translation函数：

- 功能说明：翻译解析
- 返回值：翻译解析类(解析好的)
- 参数说明：

  | 参数                       | 说明                                                         |
  | :-------------------------- | :------------------------------------------------------------ |
  | domain/localedir/languages | 同上                                                         |
  | class_                     | 翻译类：默认是GNUTranslations                                |
  | fallback                   | 是否回退，如果找不到mo文件，falllback为真返回NULLTranslations，否则抛出OSError异常<br/>默认fallback为False |
  | codeset                    | 输出翻译(msgstr)的编码                                       |

###### (3) NULLTranslations 

- 功能：无行为翻译类，默认返回原始消息msgid
- 成员：

  | 成员                       | 说明                                                         |
  | :-------------------------- | :------------------------------------------------------------ |
  | _info/ info()              | mo文件头信息(元数据)，由_parse()解析设置                     |
  | _charset / charset()       | msgstr编码，由_parse()解析头部content-type设置               |
  | _output_charset            | _()调用时对msgstr的再编码，不提供设置，由子类继承设置        |
  | _fallback / add_fallback() | 添加自定义NULLTranslations 子类，实现自定义翻译功能(回调预留) |
  | _parse()                   | mo文件解析，NULLTranslations 不提供实现，返回msgid           |
  | gettext()/ lgettext()      | 返回解析的msgstr / msgstr再编码(_output_chartset 或者系统默认) |
  | ngettext()/ lngettext()    | 暂时未搞清(英语中的复数，对应不同翻译大概)                                                   |
  | install(names)                  | 将_ , gettext, ngettext 注册到内置模块builtin，可直接使用而无需导入<br/>默认只将_注册，names可选项列表["gettext", "ngettext"] |

###### (4) GNUTranslations

- 功能：标准mo文件解析类， 继承NULLTranslations， 实现_parse函数
- 成员：

  | 成员     | 说明                                              |
  | :-------- | :------------------------------------------------- |
  | _catalog | msgid/msgstr键值对， 解析后的mo文件数据放在这里面 |
  | _parse() | 完成mo文件解析                                    |

  &nbsp;&nbsp;&nbsp;&nbsp; 注意**GNUTranslations**使用**NULLTranslations** 的初始化函数，自身不提供init入口，重写了gettext相关函数。下节讲述另一个python国际化框架[Babel](https://blog.csdn.net/weixin_39517298/article/details/121623773)。
   
   #### 二、python-Babel (pythonweb国际化)

​	&nbsp;&nbsp;&nbsp;&nbsp;[上节](https://blog.csdn.net/weixin_39517298/article/details/121593399)我们利用gettext模块进行国际化，但是翻译文件的提取和生成需要借助外界工具xgettext完成。那么babel是用来干什么的呢？[Babel](http://babel.pocoo.org/en/latest/)提供了两部分功能：一是遵照标准gettext的提取和编译工具，二是提供对各种语言环境显示名称、本地化数字和日期格式等的支持。

##### 2.1  pybabel - Babel命令行工具：

​		&nbsp;&nbsp;&nbsp;&nbsp;虽然Python标准库包含一个gettext模块，使应用程序能够进行国际化，但它要求开发人员使用GNU工具（如xgettext、msgmerge和msgfmt）构建这些目录。虽然xgettext确实支持从Python文件中提取消息，但它不知道如何处理**PythonWeb**应用程序中常见的其他类型的文件(html、js)，例如模板，也不提供简单的扩展机制来添加此类支持。

​		&nbsp;&nbsp;&nbsp;&nbsp;Babel通过提供一个框架来解决这个问题，在这个框架中，可以根据配置灵活从不同类型文件中提取消息，并且还消除了对GNU gettext工具的依赖（因为这些工具不一定在所有平台上都可用）。Babel提供的命令行工具在**babel.messages**包下，它的入口是 **babel.messages.frontend:main** ，提供了以下四个功能：

- **extract**   - 从一系列文件提取翻译，生成翻译模板pot文件（portable object，可移植对象）
- **compile** - 将po文件编译成mo文件（mo， 机器对象）
- **init**        - 根据pot文件模板创建新的翻译目录
- **update**   - 根据pot文件模板更新翻译目录

###### (1) 前提准备：

​	&nbsp;&nbsp;&nbsp;&nbsp;当通过pip安装Babel完成后，会在**PYTHON_ROOT/Scrpts**下生成一个 **pybabel.exe**， **pybabel-script.py** 文件，这是python为符合命令行生成的一个可执行文件，入口就是 babel.messages.frontend:main，使用pybabel --help查看用法

```bash
pip install Babel
pybabel --help
```

- 程序目录：


```bash
babel_
|____templates
		|____index.html
|____app.py
|____babel.cfg
```

- 文件内容：

 ```python
  # app.py 
  from gettext import translation
  import os
  
  root_dir = os.path.join(os.path.dirname(__file__), "i18n")
  
  t = translation(domain="messages", localedir=root_dir, languages=["zh"])
  _ = t.gettext
  
  py_str1 = _('Hello World -py1 !')
  py_str3 = _("""
  Hello World -py3!
  """)
  
  # templates/index.html
  <!DOCTYPE html>
  <title>{{ _("Html Title") }}</title>
  <h1>{{ _("Hello World!") }}</h1>
  ```

  

###### (2) 提取命令extract：

 - **命令格式**：pybabel extract [options] dir
 - **功能说明**：从一系列文件提取翻译，生成翻译模板pot文件
 - **命令选项**：
 
| 选项 |说明  |
|:---------|:--|
| --**charset**=CHARSET |  输出文件编码，默认UTF-8|
| **-k** keywords| 要提取消息的关键字，空格隔开（默认只从调用了gettext()，ngettext()和_()提取消息）|
|**-F** mapping_file|指明提取配置文件|
|**-o** OUTPUT|指明输出文件， 默认./messages.pot|
&nbsp;&nbsp;&nbsp;&nbsp; 配置文件告诉pybabel要从当前目录及其子目录下所有的*.py文件，templates目录及其子目录下所有的*.html文件里面搜寻可翻译的文字即所有调用gettext()，ngettext()和_()方法时传入的字符串，-k lazy_gettext来提醒pybabel要搜索该方法的调用
~~~bash
pybabel extract -k lazy_gettext  -F babel.cfg -o messages.pot .

# babel.cfg
```
[python: **.py]
[jinja2: **/templates/**.html]
```
~~~

###### (3) 初始化命令init：

 - 命令格式： pybabel init [options]
 - 功能说明：根据pot文件模板创建新的翻译目录
 - 命令选项：

| 选项 |说明  |
|:---------|:--|
|**-d** output_dir, --output-dir=OUTPUT_DIR|指定了输出目录|
|**-l** locale, --locale=LOCALE|指定了翻译语言，二级子目录|
|  **-D** domain, --domain=DOMAIN |   指定了po文件名称|
| **-i** input_file, --input-file=INPUT_FILE| 指定翻译文件模板pot文件|
  =>生成文件： **<output_dir>/\<locale>/LC_MESSAGES/\<domain>.po**
 ```bash
  pybabel init -d i18n -l zh-D messages -i messages.pot
  # => i18n/CN/LC_MESSAGES/messages.po
  # 接下来修改对应msgstr对应的翻译内容
  ```

###### (4) 编译命令compile：

​     &nbsp;&nbsp;&nbsp;&nbsp; 命令和init上述列出的选项相同，但是我们需要在(3)init生成的messages.po同级生成messages.mo文件，让gettext读取解析，直接使用-d output_dir选项，会将output_dir目录下的所有po文件都会被编译成mo文件。

```bash
pybabel compile -d i18n
```

###### (5) 增量更新命令update：

​      &nbsp;&nbsp;&nbsp;&nbsp;  如果代码中的待翻译的文字被更改过或新增，我们需要重新生成”messages.pot”翻译文件模板。此时，要是再通过`pybabel init`命令来创建po文件的话，会丢失之前已翻译好的内容，这个损失是很大的，update提供了方法，将修改及新增内容放到之前编写过的messages.po文件中。

```bash
pybabel update -i messages.pot -d i18n
```

#### 2.2 jinja2国际化

​	&nbsp;&nbsp;&nbsp;&nbsp;  jinja2 是一个可扩展的模板渲染引擎。jinja2自身提供了一部分扩展在ext.py中，他的内置扩展提供了国际化功能允许在html模板中使用{{ _("")}} 表达式来提取翻译：

###### (1) 加载扩展：

​	&nbsp;&nbsp;&nbsp;&nbsp;  jinja2使用时首先需要创建环境Envoriment， 构造时提供了extentions选项，此外还可以在初始化后通过add_extention动态添加扩展，扩展通过全路径包名识别。

```python
jinja_env = Environment(
    loader=FileSystemLoader(template_path), autoescape=True,
    extensions=['jinja2.ext.i18n']
)

jinja_env.add_extension('jinja2.ext.do')
```

###### (2) 扩展调用：

​	jinja2允许在模板取值{{}}时通过"_ 、gettext 、 ngettext"来国际化，也可以通过trans控制标签取值。

```html
{{ _("Hello World") }}
{% trans %}
	Hello World -html!
{% endtrans%}
```

   翻译内容带参数时

```python
{{ _("Hello World1, %(user)s")|format(user="HTML")}}

{# 这个标签的翻译不好用，不像pythonic代码， 建议用上面的#}
{% trans user="HTML"%}
	Hello World2, {{user}}
{% endtrans %}

 {# 新样式格式化 #} 
 {{ _('Hello World3, %(user)s!', user=name) }}
```

###### (3) 程序调用：

​	需要在模板渲染的时候，将gettext的实现传入上下文中，app.py打印index.html的内容：

```python
_ = t.gettext
template_path = os.path.join(os.path.dirname(__file__), "templates")
# 环境初始化，加载扩展
jinja_env = Environment(
    loader=FileSystemLoader(template_path), autoescape=True,
    extensions=['jinja2.ext.i18n', 'jinja2.ext.do']
)

# 模板渲染时添加gettext的实现到上下文
template_name = "index.html"
tmpl = jinja_env.get_template(template_name)
data = tmpl.render({"gettext": _})

print(data)

```
本文代码地址：[python-i18n.git](https://github.com/pienapple/python-i18n)



