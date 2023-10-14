#include "book.h"
#include "bookstore.h"
int main(void){
  BookArray* a = new BookArray();
  a->input();
  cout << "-------------------" << endl;
  a->output();
  a->Search();
  return 0;
}
