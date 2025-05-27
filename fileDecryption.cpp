#include "encrypt.h"
#include <fstream>
#include <iostream>
using namespace std;
vector<uint8_t> readEncryptedFile(const string &fileName)
{
    ifstream file;
    file.open(fileName, ios::binary);
    if (!file)
    {
        throw runtime_error("Cannot open encrypted file.");
    }
    return vector<uint8_t>((istreambuf_iterator<char>(file)), {});
}
vector<uint8_t> fileDecrypt(const vector<uint8_t>& encryptedData, const vector<uint8_t>& key)
{
    vector<uint8_t> decryptedData;
    if (encryptedData.size() % 16 != 0)
    {
        throw runtime_error("Encrypted data size is not a multiple of 16 bytes.");
    }
    // Decrypt each block
    for (size_t i = 0; i < encryptedData.size(); i += 16)
    {
        vector<uint8_t> block(encryptedData.begin() + i, encryptedData.begin() + i + 16);
        vector<uint8_t> decryptedBlock = aesDecrypt(block, key);
        decryptedData.insert(decryptedData.end(), decryptedBlock.begin(), decryptedBlock.end());
    }
    return decryptedData;
}
void removePadding(vector<uint8_t>& data)
{
    if (data.empty())
    {
        return;
    }
    uint8_t paddingLength = data.back();
    if (paddingLength < 1 || paddingLength > 16 || paddingLength > data.size())
    {
        cerr << "Warning: Invalid padding detected." << endl;
        return;
    }
    for (size_t i = data.size() - paddingLength; i < data.size(); i++)
    {
        if (data[i] != paddingLength)
        {
            cerr << "Warning: Inconsistent padding detected." << endl;
            return;
        }
    }
    data.resize(data.size() - paddingLength);
}
void saveDecryptedFile(const vector<uint8_t>& data, const string& fileName) {
    ofstream out;
    out.open(fileName, ios::binary);
    if (!out) {
        throw runtime_error("Cannot open output file for decrypted data.");
    }
    out.write(reinterpret_cast<const char*>(data.data()), data.size());
}
bool universalFileDecrypt(const string& inputFileName,const string& outputFileName,const string& password)
{
    try
    {
        vector<uint8_t> key(16, 0);
        for (size_t i = 0; i < password.length(); i++)
        {
            key[i % 16] ^= static_cast<uint8_t>(password[i]);
        }
        vector<uint8_t> encryptedData = readEncryptedFile(inputFileName);
        vector<uint8_t> decryptedData = fileDecrypt(encryptedData, key);
        removePadding(decryptedData);
        saveDecryptedFile(decryptedData, outputFileName);
        cout << "File decryption completed successfully." << endl;
        return true;
    }
    catch (const exception& e)
    {
        cerr << "Decryption failed: " << e.what() << endl;
        return false;
    }
}
