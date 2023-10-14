#include "Vaccine.h"
#include "StoreVaccine.h"

int main() {
	VaccineArray* Arr = new VaccineArray();
	Arr->input();
	cout << "-------------------" << endl;
	Arr->output();
	_getch();
	Arr->Search();
	return 0;
}