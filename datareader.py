import numpy as np
import matplotlib.pyplot as plt
from ROOT import TH1I , TFile , TDirectory, TTree, std
import sys
import os

def eventreader(evnumb , ev_tree, fout,  ph, pp , td , bl , pf , fr):
	n_ch = 32
	good_channels = [0,1,3,5,6,8,9,11,12,14,15,16,17,19,21,23,24,26,28]
	good_names = ['A_dir','Bback_dir','Bfront_dir','C1_dir','C2_dir','D1_dir','D2_dir','E','F','G','H_dir','A_att','Bback_att','Bfront_att','C1_att','C2_att','D1_att','D2_att','H_att']

	#vector of spectra
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

	dirname = "event" + str(evnumb)
	dire = fout.mkdir(dirname);
	#dire.cd();  

	for his in histos:
		#store the spectrum
		dire.WriteTObject(his)
		#evaluate peak max and position
		binmax = his.GetMinimumBin()
		maxval = his.GetBinContent(binmax)
		pp.push_back(int(binmax))
		#record baseline and its fluctuations
		bb =[]
		for b in range(1,101):
			bc = his.GetBinContent(b)
			bb.append(bc)
		ave = np.mean(bb)
		fluct = 2*np.std(bb)
		bl.push_back(float(ave))
		fir = 0
		ph.push_back(float(ave - maxval))	
		if ((ave - maxval)>10*fluct):
			fir = 1
		#evaluate FWMH and duration
		fr.push_back(int(fir))
		mh = ave - (ave - maxval)/2
		bincont =0
		fwcont =0
		for b in range(1,1020):
			bc = his.GetBinContent(b)
			#to be corrected to avoid strange patterns
			if((ave-bc) > 3*fluct):
				bincont += 1			
			if((ave-bc) > mh):
				fwcont +=1
		td.push_back(int(bincont))
		pf.push_back(int(fwcont))

	ev_tree.Fill()

	pp.clear()
	ph.clear()
	td.clear()	
	bl.clear()
	pf.clear()		
	fr.clear()

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


#event Tree
ph = std.vector( float )()
pp = std.vector( int )()
td = std.vector( int )()
bl = std.vector( float )()
pf = std.vector( int )()
fr = std.vector( int )()

ev_tree = TTree("ev_tree","Events")

ev_tree._ph = ph
ev_tree._pp = pp
ev_tree._td = td
ev_tree._bl = bl
ev_tree._pf = pf
ev_tree._fr = fr

ev_tree.Branch( 'Peakheigh', ph );
ev_tree.Branch( 'Peakposition', pp );
ev_tree.Branch( 'Totalduration', td );
ev_tree.Branch( 'Baseline', bl );
ev_tree.Branch( 'PeakFWMH', pf );
ev_tree.Branch( 'Fired', fr );

fev = TFile("events.root","UPDATE")
fout = TFile("data.root","UPDATE")

#2 - start with the loop 
for ev in range(1,n_events):
	oscommand = './dqm_plot '+str(leggifile)+' '+str(ev)+' 2900'
	#print oscommand
	os.system(oscommand)
	eventreader(ev, ev_tree, fout, ph, pp , td , bl , pf , fr)
	os.system('rm countfile.txt')
	if (ev%100==0):
		print 'processed event' + str(ev)

fev.WriteTObject(ev_tree)
fev.Close()
fout.Close()