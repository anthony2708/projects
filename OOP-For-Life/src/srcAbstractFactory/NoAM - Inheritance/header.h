#include <iostream>
#include <vector>
using namespace std;

class Cars{
public:
  virtual void output() = 0;
  virtual void moveToStore() = 0;
};

class PickUpTruck: public Cars{ //Xe bán tải
public:
  PickUpTruck(){
    cout << "A pickup truck will be created!!!" << endl;
  }
  void output(){
    cout << "A pickup truck is in production" << endl;
  }
  void moveToStore(){
    cout << "A pickup truck has been moved to store" << endl;
  }
};

class SportsCar: public Cars{ //Xe thể thao
public:
  SportsCar(){
    cout << "A sports car will be created!!!" << endl;
  }
  void output(){
    cout << "A sports car is in production" << endl;
  }
  void moveToStore(){
    cout << "A sports car has been moved to store" << endl;
  }
};

class ConvertibleCar: public Cars{ //Xe mui trần
public:  
  ConvertibleCar(){
    cout << "A convertible car will be created!!!" << endl;
  }
  void output(){
    cout << "A convertible car is in production" << endl;
  }
  void moveToStore(){
    cout << "A convertible car has been moved to store" << endl;
  }
};

class AstraZenecaVan: public Cars{
public:
    AstraZenecaVan(){
      cout << "A van for AstraZeneca vaccines will be created!!!" << endl;
    }
    void output(){
        cout << "A van for AstraZeneca vaccines is in production!!!" << endl;
    }
    void moveToStore(){
        cout << "The van for AstraZeneca vaccines has now been delivered to Government for emergency use." << endl;
    }
};

class NanoCovaxVan: public Cars{
public:
    NanoCovaxVan(){
      cout << "A van for NanoCovax vaccines will be created!!!" << endl;
    }
    void output(){
        cout << "A van for NanoCovax vaccines is in production!!!" << endl;
    }
    void moveToStore(){
        cout << "The van for NanoCovax vaccines has now been delivered to Government for emergency use." << endl;
    }
};

class PfizerVan: public Cars{
public:
    PfizerVan(){
        cout << "A van for Pfizer/BioNTech vaccines will be created!!!" << endl;
    }
    void output(){
        cout << "A van for Pfizer/BioNTech vaccines is in production!!!" << endl;
    }
    void moveToStore(){
        cout << "The van for Pfizer/BioNTech vaccines has now been delivered to Government for emergency use." << endl;
    }
};