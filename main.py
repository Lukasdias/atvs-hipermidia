from classes.controllers.xml_parser import XmlParser
from classes.views.menu import Menu

XML_PATH = './data.xml'


def main():
    xml_controller = XmlParser(XML_PATH)
    menu = Menu(xml_controller)

    menu.run_menu()


if __name__ == '__main__':
    main()
