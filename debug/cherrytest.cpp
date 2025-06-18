//cb
//cb
#include <string>
#include <iostream>
void std_print(std::string text) {
std::cout << text << std::flush;
}
void std_printnl(std::string text) {
std::cout << text << std::endl;
}
std::string std_input(std::string text) {
std::cout << text << std::flush;
std::string s;
std::getline(std::cin, s);
return s;
}
int main() {
std_print("Hello, world!");
}