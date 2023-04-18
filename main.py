from classes.xml_parser import XmlParser
from lab1.third_task import third_task

XML_PATH = './data.xml'

def main():
    xml_controller = XmlParser(XML_PATH)
    third_task(xml_controller)

if __name__ == '__main__':
    main()