#pragma once
#include "header.h"
#include "abstract.h"

class CarsArray: public Cars, public Factory{
private:
  vector<Cars*> arrCars;
  int n;
public:
  void input(){
    do{
      system("cls");
      cout << "Input the number of cars here: ";
      cin >> n;
    }while(n <= 0);
    cout << "1 - Pickup Truck, 2 - Sports Cars, 3 - Convertible Cars" << endl;
    arrCars.resize(n);
    int type;
    for (unsigned int i = 0; i < n;i++){
      cout << "Input your type of car "<< i + 1 <<  " here: ";
      do{
        cin >> type;
        cin.ignore();
      }while(type<=0 || type> 3);
      arrCars.at(i) = Factory::produceCars(static_cast<eCars>(type));      
    }
  }

  void output(){
    for (unsigned int i = 0; i < n; i++){
      arrCars.at(i)->output();
    }
  }
  void moveToStore(){
    for (unsigned int i = 0; i < n;i++){
      arrCars.at(i)->moveToStore();
    }
  }
};