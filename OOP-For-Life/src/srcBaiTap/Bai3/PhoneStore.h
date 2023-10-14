#pragma once
#include "Phone.h"

class StorePhone
{
public:
	static Phone *PhoneType(int _ID)
	{
		switch (_ID)
		{
		case 1:
			return new Samsung();
			break;
		case 2:
			return new Apple();
			break;
		case 3:
			return new Xiaomi();
			break;
		default:
			return nullptr;
			break;
		}
	}
};

class PhoneArray : public StorePhone, public Phone
{
private:
	vector<Phone *> Arr;
	int N;

public:
	void input()
	{
		do
		{
			system("cls");
			cout << "Nhap vao so luong dien thoai: ";
			cin >> N;
		} while (N < 0);
		if (N == 0)
			return;
		Arr.resize(N);
		int Type;
		cout << "Cac hang dien thoai : " << endl;
		cout << " <1> Samsung" << endl;
		cout << " <2> Apple" << endl;
		cout << " <3> Xiaomi" << endl;
		for (int i = 0; i < N; i++)
		{
			cout << "-----------------------------" << endl;
			cout << "NHAP HANG DIEN THOAI THU " << (i + 1) << ": ";
			do
			{
				cin >> Type;
				cin.ignore();
			} while (Type < 1 || Type > 3);
			Arr.at(i) = StorePhone::PhoneType(Type);
			Arr.at(i)->input();
		}
	}
	void output()
	{
		system("cls");
		for (int i = 0; i < N; i++)
		{
			Arr.at(i)->output();
			cout << "------------------------" << endl;
		}
	}
	void Search()
	{
		system("cls");
		string checkID;
		bool Found = false;
		cout << "Nhap ID dien thoai can lay thong tin: ";
		getline(cin, checkID);
		for (int i = 0; i < N; i++)
		{
			if (checkID._Equal(Arr.at(i)->getID()))
			{
				cout << "Tim thay dien thoai trong cua hang!!!" << endl;
				Found = true;
				Arr.at(i)->output();
				cout << endl;
			}
		}
		if (!Found)
			cout << "Khong tim thay dien thoai trong cua hang!!!" << endl;
	}
};
