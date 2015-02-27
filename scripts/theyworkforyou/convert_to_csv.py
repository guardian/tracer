from xml.etree import ElementTree as ET
import codecs
import time, datetime

members_xml = ET.parse('all-members-2010.xml')

attrs = ['firstname', 'lastname', 'party', 'constituency', 'fromdate', 'todate', 'house']

members = []
for member in members_xml.findall('member'):
	member = { attr: member.get(attr) for attr in attrs }
	try:
		member['fromdate'] = int(time.mktime(datetime.datetime.strptime(member['fromdate'], "%Y-%m-%d").timetuple()))
		member['todate'] = int(time.mktime(datetime.datetime.strptime(member['todate'], "%Y-%m-%d").timetuple()))
		member['fullname'] = "%s %s" % (member['firstname'], member['lastname'])
		members.append(member)
	except Exception, e:
		print 'error', member
		pass

attrs.append('fullname')

with codecs.open('members.csv', 'w', 'utf-8') as outfile:
	outfile.write(','.join(attrs) + '\n')
	for member in members:
		if member['party'] != 'unknown':
			outfile.write(','.join(['"%s"' % member[attr] for attr in attrs]) + '\n')
