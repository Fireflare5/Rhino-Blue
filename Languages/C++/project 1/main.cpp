#include <ctime>
#include <iostream>
#include <fstream>
#include <string>

using namespace std;

pair<bool,int> one_word(string password) {
    int guesses = 0;
    ifstream dic("/Users/829005/Documents/Classes/AP CSP/Rhino-Blue/Languages/C++/project 1/dictionary.txt");
    string word;
    while (dic>>word) {
        guesses++;
        if(!password.compare(word)) {
            return make_pair(true, guesses);
        }
    }
    return make_pair(false, guesses);
}

int main() {
    string password;
    bool found;
    int num_guesses;

    cout << "Enter password: ";
    getline(cin,password);
    cout << "Analyzing a one-word password ..." << endl;

    double time_start = clock();

    pair<bool, int> r = one_word(password);
    found = r.first;
    num_guesses = r.second;
    double time_end = clock();

    if(found) {
        cout << password << " found in " << num_guesses << " guesses" << endl;
    } else {
        cout << password << " NOT found in " << num_guesses << " guesses!" << endl;
    }
    cout << "Time: " << ((time_end - time_start)/CLOCKS_PER_SEC) << endl;

    return 0;
}