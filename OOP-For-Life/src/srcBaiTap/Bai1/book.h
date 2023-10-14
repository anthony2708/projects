#include <iostream>
#include <vector>
#include <string>
using namespace std;

class Book{
protected:
  int ID;
  string bookName; string author; 
  int yearPublished;
  int numPages; int type;
public:
  Book(){
    type = 0;
    numPages = 0;
  }
  virtual void input() = 0;
  virtual void output() = 0;
  int getID(){
    return ID;
  }
};

class CartoonBooks: public Book{ //Truyện tranh hoạt hình
private:
  int numParts;
public:
  CartoonBooks(){
    type = 1;
  }

  void input(){
    cout << "Nhap cac thong tin cua truyen: " << endl;
    cout << "Ma sach: "; cin >> ID;
    cout << "Ten truyen: "; cin >> bookName;
    cout << "Tac gia: "; cin >> author;
    cout << "Nam xuat ban: "; cin >> yearPublished;
    cout << "So trang: "; cin >> numPages;
    cout << "Nhap so phan: "; cin >> numParts;
  }

  void output(){
    cout << "Thong tin cua quyen " << bookName << " - " << author << endl;
    cout << "Ma sach: " << ID << endl;
    cout << "The loai: Truyen tranh hoat hinh" << endl;
    cout << "Nam xuat ban: " << yearPublished << endl;
    cout << "So trang: " <<  numPages << endl;
    cout << "So phan: " << numParts << endl;
  }  
};

class VietnameseBooks: public Book{ //Sách văn học trong nước
private:
  int numChapters;
public:
  VietnameseBooks(){
    type = 2;
  }

  void input(){
    cout << "Nhap cac thong tin cua sach: " << endl;
    cout << "Ma sach: "; cin >> ID;
    cout << "Ten sach: "; cin >> bookName;
    cout << "Tac gia: "; cin >> author;
    cout << "Nam xuat ban: "; cin >> yearPublished;
    cout << "So trang: "; cin >> numPages;
    cout << "Nhap so chuong: "; cin >> numChapters;
  }

  void output(){
    cout << "Thong tin cua quyen " << bookName << " - " << author << endl;
    cout << "Ma sach: " << ID << endl;
    cout << "The loai: Sach van hoc trong nuoc" << endl;
    cout << "Nam xuat ban: " << yearPublished << endl;
    cout << "So trang: " <<  numPages << endl;
    cout << "So chuong: " << numChapters << endl;
  }
};

class ForeignLanguageBooks: public Book{ //Sách văn học nước ngoài
private:
  int numChapters;
  string bookLanguage;
public:
  ForeignLanguageBooks(){
    type = 3;
  }

  void input(){
    cout << "Nhap cac thong tin cua sach: " << endl;
    cout << "Ma sach: "; cin >> ID;
    cout << "Ten sach: "; cin >> bookName;
    cout << "Tac gia: "; cin >> author;
    cout << "Ngon ngu xuat ban: "; cin >> bookLanguage;
    cout << "Nam xuat ban: "; cin >> yearPublished;
    cout << "So trang: "; cin >> numPages;
    cout << "Nhap so chuong: "; cin >> numChapters;
  }

  void output(){
    cout << "Thong tin cua quyen " << bookName << " - " << author << endl;
    cout << "Ma sach: " << ID << endl;
    cout << "The loai: Sach van hoc nuoc ngoai" << endl;
    cout << "Ngon ngu xuat ban: " << bookLanguage << endl;
    cout << "Nam xuat ban: " << yearPublished << endl;
    cout << "So trang: " <<  numPages << endl;
    cout << "So chuong: " << numChapters << endl;
  }
};