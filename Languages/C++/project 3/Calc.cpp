#include <iostream>
#include <string>
#include <vector>

void intrest(double &investment, double monthlyInvestment, double monthlyIntrest) {
    investment = investment * (monthlyIntrest / 100 + 1);
    investment += monthlyInvestment;
}

int main() {
    double investment = 1.00;
    double annualIncome = 0;
    double Intrest = 10.02;
    int timeFrame = 7113;
    for (int i = 0; i < timeFrame; i++) {
        for (int ii = 0; ii < 12; ii++) {
            intrest(investment, annualIncome / (12 * 2), Intrest / 12);
        }
    }
    std::cout << "Profit: " << investment << "\n";
}