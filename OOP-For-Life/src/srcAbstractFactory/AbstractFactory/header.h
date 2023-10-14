#pragma once
#include <iostream>
#include <string>
#include <vector>

using namespace std;

class Cars{
public:
  virtual void output() = 0;
  virtual void moveToStore() = 0;
};

class PickUpTruck: public Cars{ //Xe bán tải
public:
  void output(){
    cout << "A pickup truck is in production" << endl;
  }
  void moveToStore(){
    cout << "A pickup truck has been moved to store" << endl;
  }
};

class SportsCar: public Cars{ //Xe thể thao
public:
  void output(){
    cout << "A sports car is in production" << endl;
  }
  void moveToStore(){
    cout << "A sports car has been moved to store" << endl;
  }
};

class ConvertibleCar: public Cars{ //Xe mui trần
public:  
  void output(){
    cout << "A convertible car is in production" << endl;
  }
  void moveToStore(){
    cout << "A convertible car has been moved to store" << endl;
  }
};

class sVehicles{
public:
    virtual void outputVan() = 0;
    virtual void deliverToGov() = 0;
};

class AstraZenecaVan: public sVehicles{
public:
    void outputVan(){
        cout << "A van for AstraZeneca vaccines is in production!!!" << endl;
    }
    void deliverToGov(){
        cout << "The van for AstraZeneca vaccines has now been delivered to Government for emergency use." << endl;
    }
};

class NanoCovaxVan: public sVehicles{
public:
    void outputVan(){
        cout << "A van for NanoCovax vaccines is in production!!!" << endl;
    }
    void deliverToGov(){
        cout << "The van for NanoCovax vaccines has now been delivered to Government for emergency use." << endl;
    }
};

class PfizerVan: public sVehicles{
public:
    void outputVan(){
        cout << "A van for Pfizer/BioNTech vaccines is in production!!!" << endl;
    }
    void deliverToGov(){
        cout << "The van for Pfizer/BioNTech vaccines has now been delivered to Government for emergency use." << endl;
    }
};