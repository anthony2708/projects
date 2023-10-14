#pragma once
#include <iostream>
#include <vector>
#include <string>
#include <conio.h>
using namespace std;

class Phone
{
protected:
	string ID;
	string Name;
	int Year;
	int Type;

public:
	Phone()
	{
		Type = 0;
	}
	virtual void input()
	{
		cout << "Nhap vao ID dien thoai: ";
		getline(cin, ID);
		cout << "Nhap vao ten dien thoai: ";
		getline(cin, Name);
		cout << "Nhap vao nam san xuat: ";
		cin >> Year;
	}
	virtual void output() = 0;
	string getID()
	{
		return ID;
	}
};

class Samsung : public Phone
{
public:
	Samsung()
	{
		Type = 1;
	}
	void output()
	{
		cout << "ID cua dien thoai: " << ID << endl;
		cout << "Ten cua dien thoai: " << Name << endl;
		cout << "Hang dien thoai: Samsung" << endl;
		cout << "Nam san xuat: " << Year << endl;
	}
};

class Apple : public Phone
{
public:
	Apple()
	{
		Type = 2;
	}
	void output()
	{
		cout << "ID cua dien thoai: " << ID << endl;
		cout << "Ten cua dien thoai: " << Name << endl;
		cout << "Hang dien thoai: Apple" << endl;
		cout << "Nam san xuat: " << Year << endl;
	}
};

class Xiaomi : public Phone
{
public:
	Xiaomi()
	{
		Type = 3;
	}
	void output()
	{
		cout << "ID cua dien thoai: " << ID << endl;
		cout << "Ten cua dien thoai: " << Name << endl;
		cout << "Hang dien thoai: Xiaomi" << endl;
		cout << "Nam san xuat: " << Year << endl;
	}
};