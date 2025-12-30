#include <iostream>

using namespace std;

void simple(void);  //函数原型，函数声明

int main(void) 
{
	cout << "main() will call the simple() function" << endl;
	simple(); // 函数调用
	return 0;
}

void simple(void) // 函数定义
{
	cout << "I'm but a simple function." << endl;
}
