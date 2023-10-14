#pragma once
#include <iostream>
#include <vector>
#include <string>
#include <conio.h>
using namespace std;

class Vaccine {
protected:
	string ID;
	string Name;
	string Company;
	int Type;
public:
	Vaccine() {
		Type = 0;
	}	
	virtual void input() {
		cout << "Nhap vao ID vaccine: ";
		getline(cin, ID);
		cout << "Nhap vao ten vaccine: ";
		getline(cin, Name);
		cout << "Nhap vao ten cong ty san xuat: ";
		getline(cin, Company);
	}
	virtual void output() = 0;
	string getID() {
		return ID;
	}
};

class AstraZeneca : public Vaccine {
public:
	AstraZeneca() {
		Type = 1;
	}
	void output() {
		cout << "ID cua vaccine: " << ID << endl;
		cout << "Ten cua vaccine: " << Name << endl;
		cout << "Loai vaccine: AstraZeneca" << endl;
		cout << "Ten cong ty san xuat vaccine: " << Company << endl;
	}
};

class NanoCovax : public Vaccine {
public:
	NanoCovax() {
		Type = 2;
	}
	void output() {
		cout << "ID cua vaccine: " << ID << endl;
		cout << "Ten cua vaccine: " << Name << endl;
		cout << "Loai vaccine: NanoCovax" << endl;
		cout << "Ten cong ty san xuat vaccine: " << Company << endl;
	}
};

class Pfizer_BioNTech : public Vaccine {
public:
	Pfizer_BioNTech() {
		Type = 3;
	}
	void output() {
		cout << "ID cua vaccine: " << ID << endl;
		cout << "Ten cua vaccine: " << Name << endl;
		cout << "Loai vaccine: Pfizer-BioNTech" << endl;
		cout << "Ten cong ty san xuat vaccine: " << Company << endl;
	}
};