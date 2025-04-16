//cb
#include <iostream>
void print(std::string text) {//parsef1.py
std::cout << text << std::endl;//ugly
}//parsef1.py
int main(){
try {
const int x = 0;
if (x == 0 ){
print("이프문 잘대노");
}//parsef1.py
else{
print("이프문 안대노");
}//parsef1.py
print("안녕하세요! 체리블라섬!");
} catch (const std::exception& e) {
std::cerr << "Error: " << e.what() << std::endl;
return 1;
}
return 0;
}