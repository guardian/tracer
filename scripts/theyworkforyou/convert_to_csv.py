from xml.etree import ElementTree as ET
import codecs

members_xml = ET.parse('all-members.xml')

attrs = ['firstname','lastname', 'title', 'party', 'constituency', 'fromdate', 'todate', 'house']

members = []
for member in members_xml.findall('member'):
	member = { attr: member.get(attr) for attr in attrs }
	members.append(member)

with codecs.open('members.csv', 'w', 'utf-8') as outfile:
	outfile.write(','.join(attrs) + '\n')
	for member in members:
		if member['party'] != 'unknown':
			outfile.write(','.join(['"%s"' % member[attr] for attr in attrs]) + '\n')
