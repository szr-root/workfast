#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/15 11:16
# @Author  : John
# @File    : wording.py
# @Remake  :
import re

import xlrd
import os
from xlutils.copy import copy

# ----------------------------- 定义 Wording Excel -----------------------------

# Wording 文件
import xlwt

FILE_PATH = './WooPlus_WordingContent2.xlsx'

# 语言文本Sheet名字
SHEET_LANGUAGE = 'wording'

# Profile选项Sheet名字
SHEET_PROFILE_PERSONAL_DETAILS = 'profile personal details'

# 敏感词Sheet名字
SHEET_SENSITIVE = 'sensitive'

# 默认语言, 确认和Excel里的sheet名字一致
DEFAULT_LANGUAGE = 'en'

# 支持的语言, 确认和Excel里的sheet名字一致
# 如果excel有，但是这里没有，则不会生成对应的语言
SUPPORT_LANGUAGES = ['en', 'de']

# ---------- Tab页通用列定义 (后续考虑用用关键字搜索，而不是这种写死的定义)

# 列1 Wording编号
COLUMN_NO = 0

# 列4 参数
COLUMN_PARAMS = 3

# 列5 标识符
COLUMN_ID = 5

# 列6 Wording类型，plural gender
COLUMN_TYPE = 6

# 列7 注释说明
COLUMN_NOTE = 7

# ----------------------------- 定义 文件与目录 -----------------------------

# ---------- 基本文案文件

# Wording使用类名
# 比如定义为 xyz, 则dart代码使用为 xyz.of(context).helloWorld
CLASS_NAME_LOCALIZATION = 'ApplicationLocalizations'

# 输出文件夹
OUTPUT_DIR = 'test'

# localization文件
FILE_LOCALIZATION = 'localization.dart'

# localization_delegate文件
FILE_LOCALIZATION_DELEGATE = 'application_localizations_delegate.dart'

# messages_all文件
FILE_MSG_ALL = 'messages_all.dart'

# messages对应的语言文件, 编号小于 is_options_row() 的文案
FILE_MSG_LANGUAGE = 'messages_{}.dart'

# ---------- 选项类文案

# options选项数据json文件, 比如profile里的各种选项
FILE_JSON_LANGUAGE = 'dict_{}.json'

# ---------- 敏感词文案

# 敏感词 chat_security json文件
FILE_JSON_SENSITIVE_CHAT_SECURITY = 'sensitive_chat_security_{}.json'


# 敏感词 chat_security 的Wording编号范围
def is_sensitive_chat_security(wording_no):
    return wording_no >= 901000 and wording_no <= 901999


# 敏感词 chat_harass json文件
FILE_JSON_SENSITIVE_CHAT_HARASS = 'sensitive_chat_harass_{}.json'


# 敏感词 chat_harass 的Wording编号范围
def is_sensitive_chat_harass(wording_no):
    return wording_no >= 902000 and wording_no <= 902999


# 敏感词 register json文件
FILE_JSON_SENSITIVE_REGISTER = 'sensitive_register_{}.json'


# 敏感词 register 的Wording编号范围
def is_sensitive_register(wording_no):
    return wording_no >= 903000 and wording_no <= 903999


# ----------------------------- 方法 -----------------------------

# -----------------------
#      打开Excel文件
# -----------------------
def openExcel(path):
    try:
        excel = xlrd.open_workbook(path)
    except Exception as ex:
        print('Wording文件打开失败，确认文件是否存在，格式是否正常,' + ex)
    else:
        print('Wording文件打开成功')
        return excel


# -----------------------
#   解析Excel中的语言Sheet
# -----------------------
def get_language_sheet(excel):
    table_name_list = excel.sheet_names()
    if table_name_list.count == 0:
        print('Excel没有任何sheet')
        quit()
        return False

    for sheet_name in table_name_list:
        if sheet_name == SHEET_LANGUAGE:
            return True

    print('Excel中没有找到语言Sheet: ' + SHEET_LANGUAGE)
    return False


# -----------------------
#     确认输出目录存在
# -----------------------
def create_output_dir():
    if os.path.isdir(OUTPUT_DIR) == False:
        os.mkdir(OUTPUT_DIR)
    os.chdir(OUTPUT_DIR)


# -----------------------
#     解析有多少种语言
#  返回存在，且支持的语言数组
# -----------------------
def parse_languages(table):
    row_values = table.row_values(0)
    languages_list = []
    # 检查默认语言是否存在
    if DEFAULT_LANGUAGE not in row_values:
        print(SHEET_LANGUAGE + '中没有发现默认语言: ' + DEFAULT_LANGUAGE)
        quit()

    # 前提是还要当前支持该语言
    # 不是excel配置了该语言，就一定要生成的
    for title in row_values:
        if title in SUPPORT_LANGUAGES:
            print('发现支持的语言: ' + title)
            languages_list.append(title)

    return languages_list


# -----------------------
#   生成localization文件
# -----------------------
def generate_default_localization(table, language):
    obj = open(FILE_LOCALIZATION, 'w+')
    if not obj:
        print('创建 ' + FILE_LOCALIZATION + ' 文件失败')
        quit()

    # 顶部part of
    obj.write("part of '{}';".format(FILE_LOCALIZATION_DELEGATE))
    # 头部其他内容
    header = """

class {0} {{

  static Future<{0}> load(Locale locale) {{

    final String name = locale.countryCode == null ? locale.languageCode : locale.toString();
    final String localeName = Intl.canonicalizedLocale(name);
    return initializeMessages(localeName).then((bool _) {{
      Intl.defaultLocale = localeName;
      return {0}();
    }});
  }}

  static {0}? of(BuildContext context) {{
    return Localizations.of<{0}>(context, {0});
  }}
    """.format(CLASS_NAME_LOCALIZATION)
    obj.write(header)

    wording_index = None
    # 遍历每行
    for index in range(table.nrows):

        row_values = table.row_values(index)
        # testtesttest
        print(row_values)
        # 第一行是标题行
        if index == 0:
            wording_index = row_values.index(language)
            continue

        wording_no = str(row_values[COLUMN_NO]).strip()
        wording = row_values[wording_index].strip()
        wording = wording.replace('"', "\\\"")
        params = row_values[COLUMN_PARAMS].strip()
        symbol = row_values[COLUMN_ID].strip()
        wording_type = row_values[COLUMN_TYPE].strip()
        notice = row_values[COLUMN_NOTE].strip()

        if notice.find('\n'):
            notice_list = notice.split('\n')
            for index in range(len(notice_list)):
                notice_list[index] = "  // " + notice_list[index]
            notice = '\n'.join(notice_list)
        else:
            notice = "  // " + notice

        # 必须要有编号、内容、标识才生成wording
        if wording_no == '' or wording == '' or symbol == '':
            continue

        # 去除小数点
        wording_no = wording_no.split('.')[0]

        # plural, 数量区分文案
        if wording_type == 'plural':

            if params == '':
                print('编号 {} , 类型plural, 没提供参数'.format(wording_no))
                continue

            params_list = params.split(',')
            if params_list[0] != 'howMany':
                print('编号 {} , 类型plural, 第一个参数不是howMany'.format(wording_no))
                continue

            segment = wording.split('*')
            plural_list = []
            # *分割字符串，遍历数组
            for value in segment:
                value_index = segment.index(value)
                if value_index == 0:
                    if value != '':
                        plural_list.append("zero: \"{}\"".format(value))
                elif value_index == 1:
                    if value != '':
                        plural_list.append("one: \"{}\"".format(value))
                else:
                    plural_list.append("other: \"{}\"".format(value))

            if len(plural_list) < 2:
                print('编号 {} , 类型plural, 文案格式有误，请检查'.format(wording_no))
                continue

            plural_arguments = ", ".join(plural_list)
            obj.writelines([
                "\n",
                "  // 编号 {}\n".format(wording_no),
                "{}\n".format(notice),
                "  String {}({}) {{\n".format(symbol, params),
                "    return Intl.plural({}, {}, name: '{}', args: [{}]);\n".format(params_list[0], plural_arguments,
                                                                                   symbol, params),
                "  }\n"
            ])
        # gender, 性别区分文案
        elif wording_type == 'gender':

            segment = wording.split('*')
            gender_list = []
            # *分割字符串，遍历数组
            for i in range(0, len(segment)):
                value = segment[i]
                if i == 0:
                    if value != '':
                        gender_list.append("male: \"{}\"".format(value))
                    else:
                        gender_list.append("male: null")
                elif i == 1:
                    if value != '':
                        gender_list.append("female: \"{}\"".format(value))
                    else:
                        gender_list.append("female: null")
                else:
                    if value is None or value == '':
                        print('WordingNo {} , Gender类型文案的 other 为空', wording_no)
                    gender_list.append("other: \"{}\"".format(value))

            # Gender文案报警提示，要求gender做到3段式，即提供male female other3种，other是兜底保护方案
            # 防止因为客户端、服务端处理数据有误，获取不到gender值时，取other为空
            # 经过讨论，该保护暂时不考虑做在python层，而是放到excel层去确保，python仅报警
            if len(gender_list) < 3:
                print('编号 {} , 类型gender, *分段存在问题，只有{}段'.format(wording_no, len(gender_list)))

            # 如果只提供了male female，则补充other
            if len(gender_list) == 2:
                gender_list.append("other: ''")

            gender_arguments = ", ".join(gender_list)
            obj.writelines([
                "\n",
                "  // 编号 {}\n".format(wording_no),
                "{}\n".format(notice),
                "  String {}(gender, {}) {{\n".format(symbol, params),
                "    return Intl.gender(gender, {}, name: '{}', args: [gender, {}]);\n".format(gender_arguments, symbol,
                                                                                               params),
                "  }\n"
            ])
        # 普通文案
        else:
            if params == '':
                obj.writelines([
                    "\n",
                    "  // 编号 {}\n".format(wording_no),
                    "{}\n".format(notice),
                    "  String get {} {{\n".format(symbol),
                    "    return Intl.message(\"{}\", name: \"{}\");\n".format(wording, symbol),
                    "  }\n"
                ])
            else:
                obj.writelines([
                    "\n",
                    "  // 编号 {}\n".format(wording_no),
                    "{}\n".format(notice),
                    "  String {}({}) {{\n".format(symbol, params),
                    "    return Intl.message(\"{}\", name: \"{}\", args: [{}]);\n".format(wording, symbol, params),
                    "  }\n"
                ])

    obj.write('\n}')
    obj.close()


# -----------------------
# 生成localization_delegate.dart文件
# -----------------------
def generate_localization_delegate(languages):
    obj = open(FILE_LOCALIZATION_DELEGATE, 'w+')
    if not obj:
        print('创建' + FILE_LOCALIZATION_DELEGATE + '文件失败')
        quit()

    # 顶部
    obj.write("import 'package:intl/intl.dart';\n")
    obj.write("import 'package:flutter/material.dart';\n")
    obj.write("import '{}';\n".format(FILE_MSG_ALL))
    obj.write("part '{}';\n".format(FILE_LOCALIZATION))

    # 内容
    languages_list = []
    for value in languages:
        languages_list.append("'{}'".format(value))
    languages_value = ', '.join(languages_list)
    obj.write("""
class ApplicationLocalizationsDelegate extends LocalizationsDelegate<{1}> {{

  const ApplicationLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) {{
    return [{0}].contains(locale.languageCode);
  }}

  @override
  Future<{1}> load(Locale locale) {{
    return {1}.load(locale);
  }}

  @override
  bool shouldReload(LocalizationsDelegate<{1}> old) {{
    return false;
  }}
}}""".format(languages_value, CLASS_NAME_LOCALIZATION))

    obj.close()


# -----------------------
# 生成各语言的messages文件
# table - sheet对象
# language - 语言对象，比如 en、de
# 理论上可以一次for循环直接生成所有文件，但是这里不需要考虑性能问题
# 这里更重要的是要考虑逻辑清晰度，方便后来的人维护，因此每个语言单独跑一次，生成逻辑更清晰
# -----------------------
def generate_messages(table, language):
    # messages文件
    obj = open(FILE_MSG_LANGUAGE.format(language), 'w+')
    if not obj:
        print('创建' + FILE_MSG_LANGUAGE.format(language) + '文件失败')
        quit()

    # 顶部
    obj.write("import 'package:intl/intl.dart';\n")
    obj.write("import 'package:intl/message_lookup_by_library.dart';\n")

    # 类定义
    obj.write("""

final messages = MessageLookup();

class MessageLookup extends MessageLookupByLibrary {{

  get localeName => '{}';

  final messages = _createMessages();

  static Map<String, dynamic> _createMessages() => <String, Function> {{

""".format(language))

    # 文案生成, 遍历每行
    wording_index = None
    for index in range(table.nrows):

        row_values = table.row_values(index)
        # 第一行是标题行
        if index == 0:
            wording_index = row_values.index(language)
            continue

        wording_no = str(row_values[COLUMN_NO]).strip()
        wording = row_values[wording_index].strip()
        wording = wording.replace('"', "\\\"")
        params = row_values[COLUMN_PARAMS].strip()
        symbol = row_values[COLUMN_ID].strip()
        wording_type = row_values[COLUMN_TYPE].strip()

        # 必须要有编号、内容、标识才生成wording
        if wording_no == '' or wording == '' or symbol == '':
            continue

        # 写入messages文件
        write_messages_wording(obj, wording_no, wording, params, symbol, wording_type)

    obj.write('  };\n\n}')
    obj.close()


# -----------------------
#  向messages文件写入数据
# -----------------------
def write_messages_wording(message_file, wording_no, wording, params, symbol, wording_type):
    # plural, 数量区分文案
    if wording_type == 'plural' and params != '':

        params_list = params.split(',')
        if params_list[0] != 'howMany':
            print('编号 {} , 类型plural, 第一个参数不是howMany'.format(wording_no))
            return

        segment = wording.split('*')
        plural_list = []
        # *分割字符串，遍历数组
        for value in segment:
            value_index = segment.index(value)
            if value_index == 0:
                if value != '':
                    plural_list.append("zero: \"{}\"".format(value))
            elif value_index == 1:
                if value != '':
                    plural_list.append("one: \"{}\"".format(value))
            else:
                plural_list.append("other: \"{}\"".format(value))

        plural_arguments = ", ".join(plural_list)
        message_file.writelines([
            "    '{}': ({}) => Intl.plural({}, {}),\n".format(symbol, params, params_list[0], plural_arguments),
        ])
    # gender, 性别区分文案
    elif wording_type == 'gender':

        segment = wording.split('*')
        gender_list = []
        # *分割字符串，遍历数组
        for i in range(0, len(segment)):
            value = segment[i]
            if i == 0:
                if value != '':
                    gender_list.append("male: \"{}\"".format(value))
                else:
                    gender_list.append("male: null")
            elif i == 1:
                if value != '':
                    gender_list.append("female: \"{}\"".format(value))
                else:
                    gender_list.append("female: null")
            elif i == 2:
                if value is None or value == '':
                    print('WordingNo {} , Gender类型文案的 other 为空', wording_no)
                gender_list.append("other: \"{}\"".format(value))

        if len(segment) > 3:
            print('语言 {} , 文案 {} 超过了3个分段'.format(lang, wording_no))

        if len(gender_list) == 2:
            gender_list.append("other: \"\"")

        gender_arguments = ", ".join(gender_list)
        message_file.writelines([
            "    '{0}': (gender, {1}) => Intl.gender(gender, {2}),\n".format(symbol, params, gender_arguments),
        ])
    # 普通文案
    else:
        if params == '':
            message_file.writelines([
                "    '{}': () => \"{}\",\n".format(symbol, wording),
            ])
        else:
            message_file.writelines([
                "    '{}': ({}) => \"{}\",\n".format(symbol, params, wording),
            ])


# -----------------------
#  生成messages资源管理文件
# -----------------------
def generate_messages_all(languages_list):
    obj = open(FILE_MSG_ALL, 'w+')
    if not obj:
        print('创建' + FILE_MSG_ALL + '文件失败')
        quit()

    # 头部
    obj.writelines([
        "import 'package:intl/intl.dart';\n",
        "import 'package:intl/message_lookup_by_library.dart';\n",
        "import 'package:intl/src/intl_helpers.dart';\n",
    ])

    for lang in languages_list:
        obj.write("import '{}' deferred as messages_{};\n".format(FILE_MSG_LANGUAGE.format(lang), lang))

    # 内容 - 懒加载库映射定义
    obj.write("\n\ntypedef Future<dynamic> LibraryLoader();\n")
    obj.write("Map<String, LibraryLoader> _deferredLibraries = {\n")
    for lang in languages_list:
        obj.write("  '{0}': () => messages_{0}.loadLibrary(),\n".format(lang))
    obj.write("  'und': () => messages_{}.loadLibrary(),\n".format(DEFAULT_LANGUAGE))
    obj.write("};\n")

    # MessageLookup 消息映射
    obj.writelines([
        "MessageLookupByLibrary? _findExact(localeName) {\n",
        "  switch (localeName) {\n",
    ])
    for lang in languages_list:
        obj.writelines([
            "    case \"{}\":\n".format(lang),
            "      return messages_{}.messages;\n".format(lang),
        ])
    obj.writelines([
        "    case \"und\":\n".format(lang),
        "      return messages_{}.messages;\n".format(DEFAULT_LANGUAGE),
    ])
    obj.writelines([
        "    default:\n",
        "      return null;\n",
        "  }\n",
        "}\n"
    ])

    # 内容 - 其他剩下的方法
    obj.write("""

Future<bool> initializeMessages(String localeName) async {

  var availableLocale = Intl.verifiedLocale(
    localeName,
    (locale) => _deferredLibraries[locale] != null,
    onFailure: (_) => null
  );

  if (availableLocale == null) {
    return false;
  }

  var lib = _deferredLibraries[availableLocale];
  if (lib != null) {
    await lib();
  }

  initializeInternalMessageLookup(() => CompositeMessageLookup());
  messageLookup.addLocale(availableLocale, _findGeneratedMessagesFor);

  return true;
}

bool _messagesExistFor(String locale) {

  try {
    return _findExact(locale) != null;
  } 
  catch (e) {
    return false;
  }
}

MessageLookupByLibrary? _findGeneratedMessagesFor(locale) {

  var actualLocale = Intl.verifiedLocale(
      locale, 
      _messagesExistFor,
      onFailure: (_) => null
  );
  if (actualLocale == null) return null;
  return _findExact(actualLocale);
}

    """)

    obj.close()


# -----------------------
#   生成选项json数据
#   目前选项类数据基本都是profile中的
# -----------------------
def generate_options_json(table, language):
    # 对应语言的json字典选项文件
    obj = open(FILE_JSON_LANGUAGE.format(language), 'w+')
    if not obj:
        print('创建' + FILE_JSON_LANGUAGE.format(language) + '文件失败')
        quit()

    obj.write('{')

    # 文案生成, 遍历每行
    wording_index = None
    first_json = True
    for index in range(table.nrows):

        row_values = table.row_values(index)
        # 第一行是标题行
        if index == 0:
            wording_index = row_values.index(language)
            continue

        wording_no = str(row_values[COLUMN_NO]).strip()
        wording = row_values[wording_index].strip()
        wording = wording.replace('"', "\\\"")
        symbol = row_values[COLUMN_ID].strip()

        # 必须要有编号、内容、标识才生成wording
        if wording_no == '' or wording == '' or symbol == '':
            continue

        if first_json:
            first_json = False
            obj.write("\"{}\":\"{}\"".format(symbol, wording))
        else:
            obj.write(",\"{}\":\"{}\"".format(symbol, wording))
            continue

    obj.write('}')
    obj.close()


# -----------------------
#   生成敏感词json数组
#   目前只有chat_harass、chat_security、register
# -----------------------
def generate_sensitive_json(table, language):
    file_name_list = [
        FILE_JSON_SENSITIVE_CHAT_HARASS.format(language),
        FILE_JSON_SENSITIVE_CHAT_SECURITY.format(language),
        FILE_JSON_SENSITIVE_REGISTER.format(language),
    ]

    # 创建并打开文件
    file_handler_list = []
    for file_name in file_name_list:

        handler = open(file_name, 'w+')
        if not handler:
            print('创建' + file_name + '文件失败')
            quit()

        file_handler_list.append(handler)

    # 写入JSON数组头
    for file_handler in file_handler_list:
        file_handler.write('[')

    # 是否是写第一个值，标记
    file_first_list = [True, True, True]

    # Wording 语言列所在索引
    wording_index = None
    for index in range(table.nrows):

        row_values = table.row_values(index)
        # 第一行是标题行
        if index == 0:
            wording_index = row_values.index(language)
            continue

        # 通过Wording No判断是属于哪个端的敏感词
        wording_no = str(row_values[COLUMN_NO]).strip()
        wording = row_values[wording_index]
        # 必须要有编号、内容才生成wording
        if wording_no == '' or wording == '':
            continue

        # 对应数组索引
        index = None
        if is_sensitive_chat_harass(float(wording_no)):
            index = 0
        elif is_sensitive_chat_security(float(wording_no)):
            index = 1
        elif is_sensitive_register(float(wording_no)):
            index = 2

        if index is None:
            continue

        # 写入过值后就标记为false
        file_handler = file_handler_list[index]
        if file_first_list[index]:
            file_first_list[index] = False
            file_handler.write("\"{}\"".format(wording))
        else:
            file_handler.write(",\"{}\"".format(wording))

    # 文件收尾
    for file_handler in file_handler_list:
        file_handler.write(']')
        file_handler.close()


# ----------------------------- 流程 -----------------------------
if __name__ == '__main__':
    # 1, 打开文件
    excel = openExcel(FILE_PATH)
    if not excel:
        quit()

    # 2, 查找Wording所在的Sheet
    if get_language_sheet(excel) == False:
        quit()

    # 3, 创建输出目录, 并切换到该目录下
    create_output_dir()

    # 4, 解析Wording Tab有多少种可以生成的语言
    wording_table = excel.sheet_by_name(SHEET_LANGUAGE)
    languages_list = parse_languages(wording_table)
    if languages_list.count == 0:
        quit()

    # # 自动填充已存在的数据
    #
    # wb = copy(excel)
    # sheet = wb.get_sheet(1)
    # # 5, test新增一列参数
    # for index in range(1, wording_table.nrows):
    #     row_values = wording_table.row_values(index)
    #     wording_content = row_values[1].strip()
    #     wording_content = wording_content.replace('"', "\\\"")
    #     # 匹配变量
    #     pattern = re.compile('\$[a-z|A-Z]+')
    #     result = pattern.findall(wording_content)
    #     # 匹配 *
    #     gender_pattern = re.compile('\*')
    #     gender_num = gender_pattern.findall(wording_content)
    #     # print(len(result))
    #     if (len(result) == 0) and (len(gender_num) != 0):
    #         sheet.write(index, 4, ('*:%d' % (len(gender_num))))
    #
    #     elif (len(result) != 0) and (len(gender_num) == 0):
    #         sheet.write(index, 4, ('变量$:%d' % (len(result))))
    #
    #     elif (len(result) != 0) and (len(gender_num) != 0):
    #         sheet.write(index, 4, ('变量$:%d; *:%d' % (len(result), len(gender_num))))
    #
    #     else:
    #         continue
    # wb.save('./WooPlus_WordingContent2.xlsx')

    for index in range(1, wording_table.nrows):
        # 排出LA部分的内容。
        if index in range(1021, 1164):
            continue
        for i in [1, 2]:
            row_values = wording_table.row_values(index)  # 读取每一行
            wording_content = row_values[i].strip()
            wording_content = wording_content.replace('"', "\\\"")
            params = row_values[3]
            new_result_list = []

            pattern = re.compile('\$[a-z|A-Z]+')
            result = pattern.findall(wording_content)

            gender_pattern = re.compile('\*')
            gender_num = gender_pattern.findall(wording_content)

            for i in range(len(result)):
                x = result[i][1:]
                new_result = ''.join(x)
                new_result_list.append(new_result)
            # 检测wording文案中的所有变量($xxx)均在params中填写
            for i in range(len(new_result_list)):
                if new_result_list[i] not in params:
                    print('第{}行参数不匹配'.format(index + 1))
                    quit()

            # 检测wording中变量个数($,*)与params_num一致
            params_col = row_values[4]  # 新增第4列，参数个数列
            if (len(new_result_list) != 0 or len(gender_num) != 0) and params_col == '':
                print('第{}行参数不匹配'.format(index + 1))
                quit()
            if params_col != '':
                params_num = 0
                params_gender_num = 0
                params_num_pattern = re.search('\$:(\d)', params_col)
                if params_num_pattern != None:
                    params_num = params_num_pattern.group(1)

                params_gender_pattern = re.search('\*:(\d)', params_col)
                if params_gender_pattern != None:
                    params_gender_num = params_gender_pattern.group(1)

                if (len(new_result_list) != int(params_num)) or (len(gender_num) != int(params_gender_num)):
                    print('第{}行不匹配'.format(index + 1))
                    quit()

            else:
                continue

#
# # 4, 生成默认语言模板的localization
# generate_default_localization(wording_table, DEFAULT_LANGUAGE)
#
# # 5, 创建localization_delegate
# generate_localization_delegate(languages_list)
#
# # 6, 创建messages_all资源管理文件
# generate_messages_all(languages_list)
#
# # 7, 遍历各语言
# profile_table = excel.sheet_by_name(SHEET_PROFILE_PERSONAL_DETAILS)
# sensitive_table = excel.sheet_by_name(SHEET_SENSITIVE)
# for lang in languages_list:
#     # 8, 创建具体语言的messages_xx文件
#     generate_messages(wording_table, lang)
#     # 9, 创建选项json文件
#     generate_options_json(profile_table, lang)
#     # 10, 创建敏感词文件
#     generate_sensitive_json(sensitive_table, lang)
#
