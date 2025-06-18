//cb
//cb
#include <string>
#include <iostream>
void std_print(std::string text) {//parsef1.py
std::cout << text << std::flush;
}
void std_printnl(std::string text) {//parsef1.py
std::cout << text << std::endl;
}
std::string std_input(std::string text) {//parsef1.py
std::cout << text << std::flush;
std::string s;
std::getline(std::cin, s);
return s;
}
int main() {//parsef1.py
std_print("Hello, world!");
}