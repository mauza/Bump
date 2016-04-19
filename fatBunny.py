ListPrice = 548000
sqfoot = 6648

TotUnits = 6  # Total number of units in the complex
DownPP = 0.08  # Down payment percentage

#  Percentage Rates: Property Taxes, Mortgage etc... data retrieved 4/4/2016
pt = 0.0075  # Property tax for Salt Lake County Utah on average is 0.688
mg10 = 0.02625  # 10 year fixed mortgage: used if TotUnits is 4 or less
mg15 = 0.0275  # 15 year fixed mortgage: used if TotUnits is 4 or less
mg20 = 0.0325  # 20 year fixed mortgage: used if TotUnits is 4 or less
mg30 = 0.035  # 30 year fixed mortgage: used if TotUnits is 4 or less
cmg15 = 0.055  # 15 year variable mortgage: used if TotUnits is 4 or greater
cmg30 = 0.060  # 30 year variable mortgage: used if TotUnits is 4 or greater

if TotUnits > 4:
    mg15 = cmg15
    mg30 = cmg30
    DownPP = 0.25

DownPay = ListPrice * DownPP  # Down Payment total cost

# Add values for expenses paid for by Owner
Taxes = pt*ListPrice
Carport = 890
Garage = 289
Gas = 1053
Garbage = 78
Elec = 2838
Water = 840
Insurance = 1160
Maint = 0
Prkg = 0

if Gas < 0:
    Gas = sqfoot*.7325
if Elec < 0:
    Elec = sqfoot*.3932
if Water < 0:
    Water =  sqfoot*.3

# U(n) represents Unit and the number. The income generated monthly from a given Unit is the value variable
U1 = 850
U2 = 850
U3 = 850
U4 = 850
U5 = 850
U6 = 850
U7 = 0
U8 = 0
U9 = 0
U10 = 0

# expO is the total expected expenses of the Owner
expO = Taxes + Carport + Garage + Gas + Garbage + Elec + Water + Insurance + Maint + Prkg

# expT is the total expected expenses of the Tenant;
# because this liability is at risk in negociation it is being considered here
expT = Elec + Water

# TotIn Is total income for a month from each unit assuming they are rented
TotIn = U1 + U2 + U3 + U4 + U5 + U6 + U7 + U8 + U9 + U10

"""
Monthly payment formula
c = the monthly payment to ensure that the loan will be paid off in full
r = montly intrest rate
N = the number of montly payments (loan term).
P = the amount borrowed (principal)
c = (r*P)/(1-(1+r)**(-N)
"""

r = (mg30/12)
N = 360  # 30 year loan multiplied by 12months
P = ListPrice - DownPay

c = (r*P)/(1-(1+r)**(-N))

print('down payment: $' + str(round(DownPay, 2)))
print('Owner monthly expense: $' + str(round(expO/12, 2)))
print('Owner monthly expense + mortgage: $' + str(round((expO/12) + c, 2)))
print('Net monthly income: $' + str(round(((TotIn*12 - (expO + c*12))/12), 2)))
print('Gross monthly income: $' + str(TotIn))
print('Yearly Net Earnings on Investment: ' + str(round((TotIn*12 - (expO + c*12))/(ListPrice*DownPP)*100, 2)) + '%')
print('Virtual Gross Earnings to Investment: ' + str(round((TotIn*12)/(ListPrice*DownPP)*100, 2)) + '%')

'''
low = 0.0
high = balance
ans = (high + low)/2.0
x = balance
def moth(balance,annualInterestRate,ans):
    for x in range(12):
        balance = (balance-ans)*(1.0 +(annualInterestRate/12.0))
    return balance

while abs(x-0) >= 0.001:

    x = moth(balance,annualInterestRate,ans)
    if x < 0:
        high = ans
    else:
        low = ans
    ans = (high + low)/2.0
if round(ans,-1)/ans > 1:
    print('Lowest Payment: ' + str(int(round(ans, -1))))
else:
    print('Lowest Payment: ' + str(int(round(ans+10, -1))))
'''