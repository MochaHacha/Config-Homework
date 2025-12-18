from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def build_xml_tree(parent, value):
    if isinstance(value, float):#если значени число
        e = SubElement(parent, "number")#number 
        e.text = str(value)
    elif isinstance(value, str):#если значени строка
        e = SubElement(parent, "string")#string
        e.text = value
    elif isinstance(value, list):#елси список
        e = SubElement(parent, "list")#рекурсия
        for v in value:
            build_xml_tree(e, v)

def to_xml(vars_dict):#превращает словарь переменных в xml
    root = Element("config")#корневой узел
    for name, value in vars_dict.items():
        var_tag = SubElement(root, "var", name=name)#для каждой переменной созадем тег
        build_xml_tree(var_tag, value)
    
    # Генерируем  строку XML
    raw_xml = tostring(root, encoding="utf-8")
    
    # Добавление отступов
    parsed = minidom.parseString(raw_xml)
    return parsed.toprettyxml(indent="    ") # 4 пробела для отступа