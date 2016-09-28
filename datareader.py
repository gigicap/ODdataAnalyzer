import numpy as np
import matplotlib.pyplot as plt
from ROOT import TH1I , TFile , TDirectory
import sys
import os

def eventreader(evnumb):
	n_ch = 32
	good_channels = [0,1,3,5,6,8,9,11,12,14,15,16,17,19,21,23,24,26,28]
	good_names = ['A_dir','Bback_dir','Bfront_dir','C1_dir','C2_dir','D1_dir','D2_dir','E','F','G','H_dir','A_att','Bback_att','Bfront_att','C1_att','C2_att','D1_att','D2_att','H_att']

	histos =[]
	good_idx = 0
	for i in range(0,n_ch):
		if i in good_channels:
			name = "h"+str(i)
			histo = TH1I(name,good_names[good_idx],1024,0,1024)
			histos.append(histo)
			good_idx += 1

	f = open('countfile.txt', 'r')
	l_index = 0
	for line in f:
		line.strip()
		columns = line.split()
		good_idx = 0
		#print columns
		for index, element in enumerate(columns):
			if index-1 in good_channels:
				histos[good_idx].SetBinContent(l_index+1,int(element))
				good_idx += 1
		l_index += 1
	f.close()
	#print l_index
	fout = TFile("data.root","UPDATE")

	dirname = "event" + str(evnumb)
	dire = fout.mkdir(dirname);
	#dire.cd();  

	for his in histos:
		dire.WriteTObject(his)
	fout.Close()
	return;

#1 - read the number of events 
leggifile = sys.argv[1]

f = open(leggifile, 'r')

n_events = 0

for line in f:
	if not line.strip():
		continue
	li = line.strip()
	if  li.startswith("E"):
		n_events += 1

f.close()
print 'file contains :'+str(n_events)+' events.'

#2 - start with the loop 
for ev in range(1,n_events):
	oscommand = './dqm_plot '+str(leggifile)+' '+str(ev)+' 2900'
	#print oscommand
	os.system(oscommand)
	eventreader(ev)
	os.system('rm countfile.txt')
	if (ev%100==0):
		print 'processed event' + str(ev)

