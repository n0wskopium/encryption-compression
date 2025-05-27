#include <iostream>
#include <fstream>
#include <unordered_map>
#include <queue>
#include <bitset>
#include <sys/stat.h>
#include <iomanip>
#include <cstdint>
using namespace std;

struct Node {
    char ch;
    int freq;
    Node *left, *right;
    Node(char c, int f) : ch(c), freq(f), left(nullptr), right(nullptr) {}
};

struct compare {
    bool operator()(Node* l, Node* r) {
        return l->freq > r->freq;
    }
};

unordered_map<char, string> codes;
unordered_map<string, char> reverseCodes;

long getFileSize(const string& filename) {
    struct stat st;
    if (stat(filename.c_str(), &st) != 0) return -1;
    return st.st_size;
}

void buildCodes(Node* root, string str) {
    if (!root) return;
    if (!root->left && !root->right) {
        codes[root->ch] = str;
        reverseCodes[str] = root->ch;
    }
    buildCodes(root->left, str + "0");
    buildCodes(root->right, str + "1");
}

Node* buildHuffmanTree(const string &text) {
    unordered_map<char, int> freq;
    for (char c : text) freq[c]++;
    priority_queue<Node*, vector<Node*>, compare> pq;
    for (auto p : freq)
        pq.push(new Node(p.first, p.second));
    while (pq.size() > 1) {
        Node *l = pq.top(); pq.pop();
        Node *r = pq.top(); pq.pop();
        Node *merged = new Node('\0', l->freq + r->freq);
        merged->left = l;
        merged->right = r;
        pq.push(merged);
    }
    return pq.top();
}

void compress(const string& inputFile, const string& outputFile) {
    ifstream in(inputFile, ios::binary);
    if (!in) {
        cerr << "Cannot open input file.\n";
        return;
    }

    string text((istreambuf_iterator<char>(in)), istreambuf_iterator<char>());
    in.close();

    Node* root = buildHuffmanTree(text);
    codes.clear();
    buildCodes(root, "");

    ofstream out(outputFile, ios::binary);
    size_t mapSize = codes.size();
    out.write(reinterpret_cast<char*>(&mapSize), sizeof(mapSize));
    for (auto& p : codes) {
        out.put(p.first);
        uint8_t len = p.second.length();
        out.put(len);
        out.write(p.second.c_str(), len);
    }

    string encoded;
    for (char c : text) encoded += codes[c];
    uint8_t pad = (8 - encoded.length() % 8) % 8;
    out.put(pad);
    for (size_t i = 0; i < encoded.size(); i += 8) {
        string byte = encoded.substr(i, 8);
        while (byte.size() < 8) byte += '0';
        bitset<8> b(byte);
        out.put(static_cast<unsigned char>(b.to_ulong()));
    }
    out.close();

    long originalBits = text.size() * 8;
    long compressedBits = encoded.size();
    double compressionRatio = 100.0 * (1.0 - (double)compressedBits / originalBits);

    cout << "\nOriginal string: " << text << "\n";
    cout << "Compressed bit string: " << encoded << "\n";
    cout << "Original size: " << originalBits << " bits\n";
    cout << "Compressed size: " << compressedBits << " bits\n";
    cout << fixed << setprecision(2);
    cout << "Compression ratio: " << compressionRatio << "%\n";

    cout << "\nHuffman Codes:\n";
    for (auto& p : codes) {
        cout << "'" << p.first << "': " << p.second << "\n";
    }
    cout << "\nCompressed file written to '" << outputFile << "'\n";
}

void decompress(const string& inputFile, const string& outputFile, const string& originalFile = "") {
    ifstream in(inputFile, ios::binary);
    if (!in) {
        cerr << "Cannot open compressed file.\n";
        return;
    }

    size_t mapSize;
    in.read(reinterpret_cast<char*>(&mapSize), sizeof(mapSize));
    reverseCodes.clear();
    for (size_t i = 0; i < mapSize; ++i) {
        char ch = in.get();
        uint8_t len = in.get();
        string code(len, ' ');
        in.read(&code[0], len);
        reverseCodes[code] = ch;
    }

    uint8_t pad = in.get();
    string bitstream;
    while (!in.eof()) {
        unsigned char byte = in.get();
        if (in.eof()) break;
        bitstream += bitset<8>(byte).to_string();
    }
    in.close();
    if (pad > 0) bitstream.erase(bitstream.end() - pad, bitstream.end());

    string decoded, temp;
    for (char bit : bitstream) {
        temp += bit;
        if (reverseCodes.count(temp)) {
            decoded += reverseCodes[temp];
            temp.clear();
        }
    }

    ofstream out(outputFile, ios::binary);
    out << decoded;
    out.close();

    cout << "\nDecompressed string: " << decoded << "\n";

    if (!originalFile.empty()) {
        ifstream orig(originalFile, ios::binary);
        string originalContent((istreambuf_iterator<char>(orig)), istreambuf_iterator<char>());
        orig.close();
        if (originalContent == decoded)
            cout << "Verification: Success!\n";
        else
            cout << "Verification: Failed.\n";
    }

    cout << "Decompressed file written to '" << outputFile << "'\n";
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        cout << "Usage:\n";
        cout << "  " << argv[0] << " compress <input.txt> <output.huff>\n";
        cout << "  " << argv[0] << " decompress <input.huff> <output.txt> [original.txt]\n";
        return 1;
    }

    string mode = argv[1];
    if (mode == "compress") {
        compress(argv[2], argv[3]);
    } else if (mode == "decompress") {
        string originalFile = (argc == 5) ? argv[4] : "";
        decompress(argv[2], argv[3], originalFile);
    } else {
        cerr << "Unknown mode. Use 'compress' or 'decompress'.\n";
        return 1;
    }
    return 0;
}
