#!/usr/bin/env python 

from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--corpus', action='store', default='cond-mat')
parser.add_argument('-limit', type=int, default=250000)
args = parser.parse_args()

setname = args.corpus
physics = ['astro-ph','cond-mat','gr-qc','hep-ex','hep-lat','hep-ph','hep-th','math-ph','nlin','nucl-ex','nucl-th','physics','quant-ph']
if args.corpus in physics:
	setname = 'physics:'+setname

URL = 'http://export.arxiv.org/oai2'

registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)
client = Client(URL, registry)

# for record in client.listRecords(metadataPrefix='arXiv',set='physics:cond-mat'):
# 	print record[1].getField('title')

date1 = datetime.strptime('2008-1-1', '%Y-%m-%d')
date2 = datetime.strptime('2015-11-30', '%Y-%m-%d')

records = client.listRecords(metadataPrefix='oai_dc', set=setname)

Nmax = args.limit
open(args.corpus+'.txt', 'w+').close() # creates the file, clears an existing file

N = 0
for (header,metadata,aux) in records:
	title = metadata['title'][0]
	title = title.replace('\n','')
	title = title.replace('  ',' ')
	title = title.replace(': ',' : ')
	title = '<title> ' + title + ' </title>\n'
 	with open(args.corpus+'.txt','a') as myfile:
 		myfile.write(title)
	N = N+1
	print N, title
	print metadata['date'][0]
	if N == Nmax:
		break