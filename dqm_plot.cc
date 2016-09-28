//Produce plot di abbondanza canale per canale (numero di eventi che superano un trigger)
#include <vector>
#include <cstring>
#include <algorithm>
#include <iostream>
#include <fstream>
//#include <string>


//numero di canali da analizzare
#define CH 32 

using namespace std;

int main(int argc, char *argv[]){
ifstream fileInput;
ofstream f_count;

f_count.open("countfile.txt");

string line;

if(argc<4){
    cout<<"Usage: dqm_plot file_name event_number thresold"<<endl;
    return 1;
}

int evt_number = atoi(argv[2]); 
int evn_check = 0;

int trr = atoi(argv[3]);

//cout<<"Plot event number :"<<evt_number<<" thresold : "<<trr<<endl;


vector<int> event_vector[CH];

//vettore da graficare
int count_K[CH];
for (int i = 0; i < CH; ++i)
	count_K[i] = 0;

//vettore delle soglie
int trh[CH];
for (int i = 0; i < CH; ++i)
	trh[i] = trr;

// open file to search
int event_counter = -1;
int group_counter = -1;
int channel_counter = -1;


fileInput.open(argv[1]);
if(fileInput.is_open()) {
    while(!fileInput.eof()) {
        if(event_counter>evt_number) break;
        getline(fileInput, line);
        	//linee da saltare a prescindere
        	if(line.empty() || line[0]=='T' || line[0]=='F') continue;
        	//record evento
        	if(line[0]=='E'){
        		event_counter++;
        		//se non è il primo evento, registra il precedente
        		if(event_counter>0){
        			//cout<<"Fill event number: "<<event_counter<<endl;
                        //plot the event
                        if(event_counter==evt_number){
                            evn_check++;
                            for(int k = 0; k<(int)event_vector[0].size(); k++){
                                f_count<<k;
                                for (int i = 0; i < CH; ++i)  {
                                    f_count<<"\t"<<event_vector[i].at(k);
                                }
                                f_count<<endl; 
                            }                
                        }

        				for (int i = 0; i < CH; ++i)
        				{	
        				int k = 0;
        				while(k< ((int)event_vector[i].size()) &&  event_vector[i].at(k)>trh[i]) k++;
        				if(k < ((int)event_vector[i].size())) count_K[i]++;
        				}
        			}
        		//reinizializza l'evento 
        		group_counter = -1;
        		channel_counter = -1;
        		for (int i = 0; i < CH; ++i)
        			event_vector[i].clear();
        		continue;
        	}
        	//record gruppo
        	if(strncmp(line.c_str(),"################GROUP: ",22)==0){
        		group_counter++;
        		//cout<<"Reading group: "<<group_counter<<endl;
        		continue;
        	}
        	//record channel
        	if(strncmp(line.c_str(),"################CHANNEL: ",22)==0){
        		channel_counter++;    //andrà già da 0 a 23...
        		//cout<<"Reading channel: "<<channel_counter<<endl;
        		continue;
        	}     
        	//normalmente registra il canale ADC dell'evento
        	if(channel_counter<CH)
        		event_vector[channel_counter].push_back(stoi(line));
        	else continue;       
    }
    fileInput.close();
}
else cout << "Unable to open file.";

//cout<<"Done"<<endl;
//cout<<"The file contains "<<event_counter+1<<" events"<<endl;
//cout<<"with "<<channel_counter+1<<" channels in "<<group_counter+1<<" groups."<<endl;




//adesso registro count_K in un file per essere letto da gnuplot
if(evt_number==-1){
    for (int i = 0; i < CH; ++i)
        f_count<<i<<"\t"<<count_K[i]<<endl;
}


f_count.close();


return 0;
}