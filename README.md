# ODdataAnalyzer
Data analyzer for object dump files

Da usare su dati già decodificati (ASCII) 
Dipendenze:
compilatore g++
python (>= 2.7)
ROOT (con modulo pyROOT attivo)

Istruzioni:

1. clonare: git clone https://github.com/gigicap/ODdataAnalyzer.git
2. compilare il file C++: g++ -o dqm_plot dqm_plot.cc
3. eseguire lo script python: python datareader.py [nome_file_decodificato.txt]

L'output è un file root contenente tante cartelle quanti gli eventi. Ogni cartella contiene uno spettro per ogni canale attivo. La tabella di conversione dei canali si trova nelle prime righe dello script python e può essere modificata a seconda delle esigenze.

