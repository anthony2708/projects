#pragma once
#include "Vaccine.h"

class StoreVaccine {
public:
	static Vaccine* VaccineType(int _ID) {
		switch (_ID)
		{
		case 1:
			return new AstraZeneca();
			break;
		case 2:
			return new NanoCovax();
			break;
		case 3:
			return new Pfizer_BioNTech();
			break;
		default:
			return nullptr;
			break;
		}
	}
};

class VaccineArray : public StoreVaccine, public Vaccine {
private:
	vector<Vaccine*> Arr;
	int N;
public:
	void input() {
		do {
			system("cls");
			cout << "Nhap vao so luong vaccine co trong kho: ";
			cin >> N;
		} while (N < 0);
		if (N == 0) return;
		Arr.resize(N);
		int Type;
		cout << "Cac loai Vaccine co trong kho: " << endl;
		cout << " <1> AstraZeneca" << endl;
		cout << " <2> NanoCovax" << endl;
		cout << " <3> Pfizer-BioNTech" << endl;
		for (int i = 0; i < N; i++) {
			cout << "-----------------------------" << endl;
			cout << "NHAP LOAI VACCINE THU " << (i + 1) << ": ";
			do {
				cin >> Type;
				cin.ignore();
			} while (Type < 1 || Type > 3);
			Arr.at(i) = StoreVaccine::VaccineType(Type);
			Arr.at(i)->input();
		}
	}
	void output() {
		system("cls");
		for (int i = 0; i < N; i++) {
			Arr.at(i)->output();
			cout << "------------------------" << endl;
		}
	}
	void Search() {
		system("cls");
		string checkID;
		bool Found = false;
		cout << "Nhap ID vaccine can lay thong tin: ";
		getline(cin, checkID);
		for (int i = 0; i < N; i++) {
			if (checkID._Equal(Arr.at(i)->getID())) {
				cout << "Tim thay vaccine trong kho!!!" << endl;
				Found = true;
				Arr.at(i)->output();
				cout << endl;
			}
		}
		if (!Found)
			cout << "Khong tim thay vaccine trong kho!!!" << endl;
	}

};