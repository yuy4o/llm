#include <iostream>
using namespace std;

long double prob(unsigned int numbers, unsigned int picks);

int main(void)
{	
	cout << "Enter the total number of choices on the game card and the number of picks allowed: " << endl;
	unsigned int total, choices;
	while ((cin >> total >> choices) && choices <= total)
	{
		cout << "You have one chance in " << prob(total, choices) << " of winning" << endl;
		cout << "Please enter next two numbers or q-key to quit: " << endl;
	}
	cout << "Bye!" << endl;	
	return 0;
}

long double prob(unsigned int numbers, unsigned int picks)
{
	double n, p;
	long double result = 1.0;
	for (n = numbers, p=picks; p>0; n--, p--)
		result = result * n/p;
	return result;
}
