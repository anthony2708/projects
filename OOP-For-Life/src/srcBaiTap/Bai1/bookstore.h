#include "book.h"

enum eBook{
  CARTOON = 1,
  VIETNAMESE = 2,
  FOREIGN = 3
};

class BookStore{ //Lớp quản lý thông tin sách - Factory Method
public:
  BookStore(){}
  ~BookStore(){}
  static Book* bookInfo(eBook _typeID){
    switch (_typeID){
      case CARTOON:
        return new CartoonBooks();
        break;
      case VIETNAMESE:
        return new VietnameseBooks();
        break;
      case FOREIGN:
        return new ForeignLanguageBooks();
        break;
      default:
        return NULL;
        break;
    }
  }
};

class BookArray: public Book, public BookStore{ //Lưu mảng để chứa lượng sách trong hiệu sách
private: //private vẫn được
  vector<Book*> arrBook;
  int n;
public:
  void input(){
    do{
      system("cls");
      cout << "Nhap so luong sach cua hieu sach: "; 
      cin >> n;
    } while(n <= 0);

    cout << "Hieu sach co: Truyen tranh(1), Sach van hoc(2), Sach ngoai van(3)" << endl;
    arrBook.resize(n);
    int type = 0;
    for (unsigned int i = 0; i < n; i++){
      cout << "--> NHAP THE LOAI QUYEN SACH THU " << i + 1 << ": ";
      do{
        cin >> type;
      }while(type <= 0 || type > 3);
      arrBook.at(i) = BookStore::bookInfo(static_cast<eBook>(type));
      arrBook.at(i)->input();
    }
  }
  void output(){
    for (unsigned int i = 0; i < n;i++){
      arrBook.at(i)->output();
      cout << "------------------------" << endl;
    }
  }
  void Search(){
    cout << "Nhap ma sach can lay thong tin: ";
    int checkID; cin >> checkID;
    for (unsigned int i = 0; i < n;i++){
      if (checkID == arrBook.at(i)->getID()){
        cout << "Tim thay quyen sach!!!" << endl;
        arrBook.at(i)->output();
        cout << endl;
      }
    }
  }
};
