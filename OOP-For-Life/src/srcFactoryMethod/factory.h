#pragma once
#include "header.h"

enum eCars{
  PICKUP_TRUCK = 1,
  SPORTS = 2,
  CONVERTIBLE = 3
};

class CarsFactory{
public:
  static Cars* produceCars(eCars _carsID){
    switch (_carsID)
    {
      case 1: return new PickUpTruck();
      case 2: return new SportsCar();
      case 3: return new ConvertibleCar();
      default: return NULL;
    }
  }
};

class CarsArray: public Cars, public CarsFactory{
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
      arrCars.at(i) = CarsFactory::produceCars(static_cast<eCars>(type));      
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