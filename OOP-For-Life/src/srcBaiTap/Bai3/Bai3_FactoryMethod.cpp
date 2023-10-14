#include "Phone.h"
#include "PhoneStore.h"

int main()
{
	PhoneArray *Arr = new PhoneArray();
	Arr->input();
	cout << "-------------------" << endl;
	Arr->output();
	_getch();
	Arr->Search();
	return 0;
}
