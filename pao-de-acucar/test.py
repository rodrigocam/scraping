from lxml import etree

# referÊncia https://stackoverflow.com/questions/3978068/how-to-check-if-the-two-xml-files-are-equivalent-with-python# referÊncia 
tree1 = etree.parse('/home/Downloads/paodeacucar_06-10-2017.xml')
tree2 = etree.parse('/home/Downloads/paodeacucar_09-10-2017.xml') 

print(set(tree1.getroot().itertext()) == set(tree2.getroot().itertext()))