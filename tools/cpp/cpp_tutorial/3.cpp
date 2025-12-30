#include <iostream>

using namespace std;

void n_chars(char c, int n);

int main(void)
{
	cout << "Enter a character: ";
	char ch;
	cin >> ch;
	
	while (ch != 'q')
	{
		cout << "Enter a integer: ";
		int times;
		cin >> times;
		n_chars(ch, times);
		cout << endl;
		cout << "Enter another character or press q_key to quit: ";
		cin >> ch;
	}
	return 0;
}

void n_chars(char c, int n)
{
	while (n-- > 0)
		cout << c; 
}
