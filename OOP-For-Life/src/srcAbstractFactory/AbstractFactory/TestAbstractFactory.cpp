#include "cararray.h"
#include "vanarray.h"

int main(void){
  //Khu vực xe kinh doanh
  CarsArray* a = new CarsArray();
  a->input();
  cout << "_______________" << endl;
  a->output();
  cout << "_______________" << endl;
  a->moveToStore();
  cout << endl;
  
  //Khu vực xe chuyên dụng cho Bộ Y tế
  VansArray* b = new VansArray();
  b->input();
  cout << "________________" << endl;
  b->outputVan();
  cout << "________________" << endl;
  b->deliverToGov();
  cout << endl;

  return 0;
}