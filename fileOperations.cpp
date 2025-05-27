#include "encrypt.h"
#include <fstream>
#include <iostream>
using namespace std;
vector<uint8_t> readFileInBinary(const string &name)
{
    ifstream file;
    file.open(name,ios::binary);
    if(!file)
        throw runtime_error("Cannot open input file.");
    return vector<uint8_t>((istreambuf_iterator<char>(file)),{});
}

void pad(vector<uint8_t> &data,size_t blockSize)
{
    size_t padding=blockSize-(data.size()%blockSize);
    if(padding==0)
        padding=blockSize;
    data.insert(data.end(),padding,static_cast<uint8_t>(padding));
}

vector<uint8_t> fileEncrypt(vector<uint8_t> &data,const vector<uint8_t> &key)
{
    vector<uint8_t> encryptData;
    for(size_t i=0;i<data.size();i+=16)
    {
            vector<uint8_t> block(data.begin()+i,data.begin()+i+16);
            vector<uint8_t> encryptedBlock=aesEncrypt(block,key);
            encryptData.insert(encryptData.end(),encryptedBlock.begin(),encryptedBlock.end());
    }
    return encryptData;
}

void saveInFile(vector<uint8_t> &data,const string &name)
{
    ofstream out;
    out.open(name,ios::binary);
    if(!out)
        throw runtime_error("Cannot open output file.");
    out.write(reinterpret_cast<const char*>(data.data()),data.size());
}
bool encryptFile(const string& inputFileName,const string& outputFileName,const string& password)
{
    try
    {
        vector<uint8_t> key(16, 0);
        for (size_t i = 0; i < password.length(); i++)
        {
            key[i % 16] ^= static_cast<uint8_t>(password[i]);
        }
        vector<uint8_t> fileData = readFileInBinary(inputFileName);
        pad(fileData, 16);
        vector<uint8_t> encryptedData = fileEncrypt(fileData, key);
        saveInFile(encryptedData, outputFileName);
        return true;
    }
    catch (const exception& e)
    {
        cerr << "Encryption failed: " << e.what() << endl;
        return false;
    }
}
