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

int main(void){
  PickUpTruck* a = new PickUpTruck();
  a->output();
  ConvertibleCar* c = new ConvertibleCar();
  c->output();
}