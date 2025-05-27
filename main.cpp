#include "encrypt.h"
#include <iostream>
#include <string>
using namespace std;
int main(int argc, char* argv[]) {
    if (argc != 5) {
        cerr << "Usage: " << argv[0] << " <encrypt/decrypt> <input> <output> <password>\n";
        return 1;
    }
    string mode(argv[1]);
    string input(argv[2]);
    string output(argv[3]);
    string password(argv[4]);

    if (mode == "encrypt") {
        return encryptFile(input, output, password) ? 0 : 1;
    } else {
        return universalFileDecrypt(input, output, password) ? 0 : 1;
    }
}
