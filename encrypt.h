#ifndef ENCRYPT_H
#define ENCRYPT_H

#include <vector>
#include <string>
#include <cstdint>
#include <array>
#include <stdexcept>
#include <fstream>
using namespace std;

extern const uint8_t sBox[256];
extern const uint8_t invSBox[256];
extern const uint8_t Rcon[11];

void saveInFile(vector<uint8_t> &data,const string &name);
void pad(vector<uint8_t> &data,size_t blockSize=16);
vector<uint8_t> readFileInBinary(const string& name);
vector<uint8_t> fileEncrypt(vector<uint8_t> &data,const vector<uint8_t> &key);
bool encryptFile(const string& inputFileName,const string& outputFileName,const string& password); //Universal function for encryption

vector<uint8_t> aesEncrypt(const vector<uint8_t>& block, const vector<uint8_t>& key);
void subBytes(array<array<uint8_t,4>,4>& state);
void shiftRows(array<array<uint8_t,4>,4>& state);
void addRoundKey(array<array<uint8_t,4>,4>& state, const vector<uint8_t>& roundKey, int round);
vector<uint8_t> keyExpansion(const vector<uint8_t> &key);
vector<uint8_t> RotWord(const vector<uint8_t>& word);
vector<uint8_t> SubWord(const vector<uint8_t>& word);

void invSubBytes(array<array<uint8_t, 4>, 4>& state);
void invShiftRows(array<array<uint8_t, 4>, 4>& state);
void invMixColumns(array<array<uint8_t, 4>, 4>& state);
void addRoundKey(array<array<uint8_t, 4>, 4>& state, const vector<uint8_t>& roundKey, int round);
uint8_t gmul(uint8_t a, uint8_t b);
vector<uint8_t> keyExpansion(const vector<uint8_t>& key);
vector<uint8_t> aesDecrypt(const vector<uint8_t>& encryptedBlock, const vector<uint8_t>& key);

vector<uint8_t> readEncryptedFile(const string &fileName);
vector<uint8_t> fileDecrypt(const vector<uint8_t>& encryptedData, const vector<uint8_t>& key);
void removePadding(vector<uint8_t>& data);
void saveDecryptedFile(const vector<uint8_t>& data, const string& fileName);

bool universalFileDecrypt(const string& inputFileName,const string& outputFileName,const string& password);

#endif
