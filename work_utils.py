#Author: Joshua McLaughlin
#written to take established, single purpose code
#and make it usable for more general usage.

import re
import datetime
import os
import shutil
import sys
sys.path.append('C:\Python34\Lib\pyperclip-1.3')


def list_append(seperator=True):
  '''
  This reads a file locally and turns a list of values into a list usable in a SQL select statement.
  The optional seperator determines if the values should be enclosed with quotation marks.
  '''
  value_list = []
  import pyperclip
  
  #change this to parameter
  foo = open('C:/Users/jmclaughlin/Desktop/list_append.txt','r+')
  
  for line in foo:
    value_list.append(line.strip())
  
  if not seperator:
    #remove [ ] from python list
    pyperclip.copy('('+re.sub("'","",str(value_list))[1:-1]+')')
    spam = pyperclip.paste()
  else:
    pyperclip.copy('('+str(value_list)[1:-1]+')')
    spam = pyperclip.paste()

def new_match_request(project_name):
  '''
  Script that launches a new "match request" project.
  Template for a match request was changed and this is no longer used.
  
  To update this I'll need to remove references to specific files and build objects
  to customize the new project
  '''
  table_name = "JM_MR_"++project_name+'_'+datetime.datetime.now().strftime("%Y%m%d")
  menaMatch = table_name+"_MENA"
  mephMatch = table_name+"_MEPH"
  folder = 'C:\\Users\\jmclaughlin\\Documents\\MATCH REQUESTS\\'+(datetime.datetime.now()).strftime("%Y%m%d")
  
  if not os.path.exists(folder):
  os.makedirs(folder)
  #create the sql file
  #copy the sql template to the new folder
  sql_location = folder+"/"+table_name+".sql"
  sql_template = 'C:/Users/jmclaughlin/encuity/new_adhoc.txt'
  shutil.copyfile(sql_template,sql_location)

def new_adhoc(project_name, specialty_list):
  '''
  Script that launches a new ad hoc project.
  Template changed, moved toward keeping work on shared drives so this is no longer used.
  '''
  date = datetime.datetime.now()
  now = date.strftime("%Y-%m-%d")
  basePath = "C:/Users/jmclaughlin/Documents/AD HOC/"	
  folder = basePath + date.strftime("%B%y").upper() + ' ' + project_name
  if not os.path.exists(folder):
  os.makedirs(folder)
  table_name = "JM_"+project_name+"_"+date.strftime("%Y%m%d").upper()
  keys = {
  'table_name': table_name,
  'specs': specialty_list,
  'now': now
  }
  #copy the email template into the new folder
  email_location = folder+"/"+table_name+".html"
  email_template = 'C:/Users/jmclaughlin/encuity/email_template.txt'
  shutil.copyfile(email_template,email_location)
  #create the sql file
  #copy the sql template to the new folder
  sql_location = folder+"/"+table_name+".sql"
  sql_template = 'C:/Users/jmclaughlin/encuity/new_adhoc.txt'
  shutil.copyfile(sql_template,sql_location)
  #replace the sql template with the formated string.
  with open(sql_location,'r+') as sql:
  sql_text = sql.read()
  sql.seek(0)
  sql.truncate()
  sql_write = sql_text.format(**keys)
  sql.write(sql_write)
  #copy the about.txt file
  shutil.copyfile('C:/Users/jmclaughlin/encuity/about.txt',folder+'/about.txt')

def kol_xml_parse(input_xml, output_authors, output_pubtypes):
  '''
  Reads xml files pubmed MeSH search for processing that's later finished in SQL server
  '''
  import xml.etree.ElementTree as ET
  tree = ET.parse(input_xml)
  root = tree.getroot()
  current_pmid = ''
  with open(output_authors, 'w', encoding='UTF-8') as output_file:
  output_file.write('PMID\tLNAME\tFNAME\tMNAME\tARTICLE_NAME\tAUTHOR_NUMBER\n')
  for child in root:
  current_pmid = child.find('.//PMID').text
  article_title = child[0].find('.//ArticleTitle').text
  author_number = 1
  for grand_child in child.iter('Author'):
  #for great_grand_child in grand_child:
  try:
  last_name = grand_child.find('LastName').text
  except AttributeError:
  last_name = ''
  try:
  first_name = grand_child.find('ForeName').text
  except AttributeError:
  first_name = ''
  try:
  initials = grand_child.find('Initials').text
  except AttributeError:
  initials = ''
  output_file.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(current_pmid, last_name, first_name, initials, article_title, author_number))
  author_number += 1
  output_file.close()
  with open(output_pubtypes, 'w', encoding = 'utf-8') as out_file:
  for child in root:
  pmid = child[0][0].text
  for journal_types in child.findall('./MedlineCitation/Article/PublicationTypeList/PublicationType'):
  #read the journal type
  string = journal_types.text
  #we wanted to roll it into two categories for simplification
  if string in ['Clinical Trial', 'Clinical Trial Phase I', 'Clinical Trial Phase II', 'Clinical Trial Phase III', 'Controlled Clinical Trial']:
  string = 'CLINICAL TRIALS'
  else:
  string = 'PUBLICATION'
  out_file.write('{}\t{}\n'.format(pmid, string))
  out_file.close()
