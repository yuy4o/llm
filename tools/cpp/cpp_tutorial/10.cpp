#include <iostream>
using namespace std;

char *buildstr(char c, int n);
int main()
{
  char ch;
  int times;
  cout << "Enter a character: "<< endl;
  cin >> ch;
  cout << "Enter an integer: " <<endl;
  cin >>times;
   
  char *ps = buildstr(ch, times);
  cout << ps << endl;
  delete []ps;
  return 0;
}

char *buildstr(char c, int n)
{
  char *ptsr =  new char[n+1];
  ptsr[n] = '\0';
  for(int i=0; i<n; i++)
    ptsr[i] = c;
  return ptsr;
}
