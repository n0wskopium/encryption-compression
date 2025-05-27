#include "encrypt.h"
#include <array>
#include <stdexcept>
const uint8_t sBox[256] =
{
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
};
const uint8_t Rcon[11] = {
    0x00, 0x01, 0x02, 0x04, 0x08,
    0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
};
void mixColumns(array<array<uint8_t, 4>, 4>& state)
{
    for (int col = 0; col < 4; col++)
    {
        uint8_t a[4], b[4];
        for (int row = 0; row < 4; row++)
        {
            a[row] = state[row][col];
            b[row] = (state[row][col] << 1) ^ ((state[row][col] & 0x80) ? 0x1b : 0x00);
        }
        state[0][col] = b[0] ^ a[1] ^ b[1] ^ a[2] ^ a[3];
        state[1][col] = a[0] ^ b[1] ^ a[2] ^ b[2] ^ a[3];
        state[2][col] = a[0] ^ a[1] ^ b[2] ^ a[3] ^ b[3];
        state[3][col] = a[0] ^ b[0] ^ a[1] ^ a[2] ^ b[3];
    }
}
void subBytes(array<array<uint8_t, 4>, 4>& state)
{
    for (int row = 0; row < 4; row++)
    {
        for (int col = 0; col < 4; col++)
        {
            state[row][col] = sBox[state[row][col]];
        }
    }
}
void shiftRows(array<array<uint8_t, 4>, 4>& state)
{
    uint8_t temp = state[1][0];
    state[1][0] = state[1][1];
    state[1][1] = state[1][2];
    state[1][2] = state[1][3];
    state[1][3] = temp;
    temp = state[2][0];
    state[2][0] = state[2][2];
    state[2][2] = temp;
    temp = state[2][1];
    state[2][1] = state[2][3];
    state[2][3] = temp;
    temp = state[3][3];
    state[3][3] = state[3][2];
    state[3][2] = state[3][1];
    state[3][1] = state[3][0];
    state[3][0] = temp;
}
void addRoundKey(array<array<uint8_t, 4>, 4>& state, const vector<uint8_t>& roundKey, int round)
{
    for (int col = 0; col < 4; col++)
    {
        for (int row = 0; row < 4; row++)
        {
            state[row][col] ^= roundKey[round * 16 + col * 4 + row];
        }
    }
}

vector<uint8_t> SubWord(const vector<uint8_t>& word)
{
    vector<uint8_t> result(4);
    for (int i = 0; i < 4; ++i)
        result[i] = sBox[word[i]];
    return result;
}
vector<uint8_t> RotWord(const vector<uint8_t>& word)
{
    return { word[1], word[2], word[3], word[0] };
}
vector<uint8_t> keyExpansion(const vector<uint8_t> &key)
{
    if(key.size()!=16)
        throw invalid_argument("Key must be 16 bytes for AES-128 Encryption");
    vector<uint8_t> expandedKey(176);
    for (int i = 0; i < 16; ++i)
        expandedKey[i] = key[i];
    int bytesGenerated = 16;
    int rconIteration = 1;
    vector<uint8_t> temp(4);
    while (bytesGenerated < 176)
    {
        for (int i = 0; i < 4; ++i)
            temp[i] = expandedKey[bytesGenerated - 4 + i];
        if (bytesGenerated % 16 == 0)
        {
            temp = RotWord(temp);
            temp = SubWord(temp);
            temp[0] ^= Rcon[rconIteration++];
        }
        for (int i = 0; i < 4; ++i)
        {
            expandedKey[bytesGenerated] = expandedKey[bytesGenerated - 16] ^ temp[i];
            bytesGenerated++;
        }
    }
    return expandedKey;
}
vector<uint8_t> aesEncrypt(const vector<uint8_t>& block, const vector<uint8_t>& key)
{
    if (block.size() != 16 || key.size() != 16)
    {
        throw runtime_error("Block and key must be 16 bytes for AES-128");
    }
    array<array<uint8_t, 4>, 4> state{};   //state
    for (int col = 0; col < 4; col++)
    {
        for (int row = 0; row < 4; row++)
        {
            state[row][col] = block[col * 4 + row];     //filling the data from source block column wise in 4*4 matrix called state
        }
    }
    vector<uint8_t> expandedKey = keyExpansion(key);
    addRoundKey(state, expandedKey, 0);
    for (int round = 1; round < 10; round++)
    {
        subBytes(state);
        shiftRows(state);
        mixColumns(state);
        addRoundKey(state, expandedKey, round);
    }
    subBytes(state);
    shiftRows(state);
    addRoundKey(state, expandedKey, 10);
    vector<uint8_t> result(16);
    for (int col = 0; col < 4; col++)
    {
        for (int row = 0; row < 4; row++)
        {
            result[col * 4 + row] = state[row][col];
        }
    }
    return result;
}
