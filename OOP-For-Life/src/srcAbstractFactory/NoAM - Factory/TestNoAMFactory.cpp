#include "factory.h"

int main(void){
  CarsArray* a = new CarsArray();
  a->input();
  cout << "_______________" << endl;
  a->output();
  cout << "_______________" << endl;
  a->moveToStore();
  return 0;
}