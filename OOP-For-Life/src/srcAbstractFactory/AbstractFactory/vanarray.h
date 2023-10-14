#pragma once
#include "header.h"
#include "abstract.h"

class VansArray: public sVehicles, public Factory{
private:
    vector<sVehicles*> arrVans;
    int n;
public:
    void input(){
    do{
      system("cls");
      cout << "Input the number of vans needed to deliver here: ";
      cin >> n;
    }while(n <= 0);
    cout << "1 - AstraZeneca, 2 - NanoCovax, 3 - Pfizer/BioNTech" << endl;
    arrVans.resize(n);
    int type;
    for (unsigned int i = 0; i < n;i++){
      cout << "Input your type of vaccine "<< i + 1 <<  " here: ";
      do{
        cin >> type;
        cin.ignore();
      }while(type<=0 || type> 3);
      arrVans.at(i) = Factory::produceVans(static_cast<eVans>(type));      
    }
  }

  void outputVan(){
      for (unsigned int i = 0; i < n;i++){
          arrVans.at(i)->outputVan();
      }
  }
  void deliverToGov(){
      for (unsigned int i = 0; i < n; i++){
          arrVans.at(i)->deliverToGov();
      }
  }
};