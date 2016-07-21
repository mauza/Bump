import requests
import BeautifulSoup as BS
import json

def calc(mlsNum, mortgage):
    #initialize the array that whill house all the data to be passed back to the template
    infoArray = []
    
    #request the json data and hold it in a variable
    try:
        mls = json.loads(requests.get('http://v9services.utahrealestate.com/property-search/listing-details?prop_class=multi&listno='+mlsNum).text)
    except:
        return ["I'm sorry, ", "I was unable to find that MLS number."]
    if mls is None:
        return ["I'm sorry, ", "I encountered an error"]
        
    #This is the zillow peice where we are mainly concerned with rent estimate
    address = mls['data']['address']
    city = mls['data']['city_name']
    state = mls['data']['state']
    try:
        zillow = BS.BeautifulSoup(requests.get(
            'http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=X1-ZWz19scygcl7gr_2uji4&address='
            + address +'&citystatezip=' + city + '%2C+'+ state + '&rentzestimate=true').text)
        zrent = zillow.find('rentzestimate').find('amount').text
        zprice = zillow.find('zestimate').find('amount').text
    except:
        infoArray.append(["WAS NOT ABLE TO ACCURATELY ESTIMATE RENT","!"])
        zrent = 300
    
    #http://v9services.utahrealestate.com/property-search/listing-details?prop_class=multi&listno=1385322
    
    #getting needed data from json   
    ListPrice = float(mls['data']['listprice'])
    sqfoot = float(mls['data']['tot_sqf'])
    TotUnits = float(mls['data']['tot_units'])
    unitRent = float(zrent)
    unitnum = float(mls['data']['tot_units'])
    
    # TotIn Is total income for a month from each unit assuming they are rented
    TotIn = TotUnits*unitRent
    
    DownPP = 0.08  # Down payment percentage
    #  Percentage Rates: Property Taxes, Mortgage etc... data retrieved 4/4/2016
    pt = 0.0075  # Property tax for Salt Lake County Utah on average is 0.688
    mg = [[0.02625,0.02625], [0.0275,0.055], [0.035,0.060]]  # 10 year fixed mortgage: used if TotUnits is 4 or less
    mgYears = int(mortgage)
    mgType = 0;
    if (unitnum>4):
        mgType = 1
        DownPP = 0.254
        
    DownPay = ListPrice * DownPP
    
    # Add values for expenses paid for by Owner
    ReporTax = 0
    Taxes = pt*ListPrice
    Carport = 0
    Garage = 0
    Gas = 0
    Garbage = 0
    Elec = 0
    Water = 0
    Insurance = 0
    Maint = 0
    Other = 0
    
    if Gas == 0:
        Gas = sqfoot*.7325
    if Elec == 0:
        Elec = sqfoot*.3932
    if Water == 0:
        Water =  sqfoot*.3
    if Garbage == 0:
        Garbage = 60*12
    if Insurance == 0:
        Insurance = 50*12
    if Maint == 0:
        Maint = (float(TotIn)/10)*12
    if TotIn == 0:
        TotIn = 550*2
        
    # expO is the total expected expenses of the Owner
    expO = Taxes + Carport + Garage + Gas + Garbage + Elec + Water + Insurance + Maint + Other
    
    # expT is the total expected expenses of the Tenant;
    # because this liability is at risk in negociation it is being considered here
    expT = Elec + Water
    
    # TotIn Is total income for a month from each unit assuming they are rented
    #TotIn = U1 + U2 + U3 + U4 + U5 + U6 + U7 + U8 + U9 + U10
    
    """
    Monthly payment formula
    c = the monthly payment to ensure that the loan will be paid off in full
    r = montly intrest rate
    N = the number of montly payments (loan term).
    P = the amount borrowed (principal)
    c = (r*P)/(1-(1+r)**(-N)
    """
    
    r = (mg[mgYears][mgType]/12)
    N = 360  # 30 year loan multiplied by 12months
    P = ListPrice - DownPay
    c = (r*P)/(1-(1+r)**(-N))
    
    infoArray.append(["MLS:  ",mlsNum])
    infoArray.append(["ReportTax: $",str(ReporTax)])
    infoArray.append(["Taxes:  $",str(Taxes)])
    infoArray.append(["Carport:  $",str(Carport)])
    infoArray.append(["Garage:  $",str(Garage)])
    infoArray.append(["Gas:  $",str(Gas)])
    infoArray.append(["Garbage:  $",str(Garbage)])
    infoArray.append(["Elec:  $",str(Elec)])
    infoArray.append(["Water:  $",str(Water)])
    infoArray.append(["Insurance:  $",str(Insurance)])
    infoArray.append(["Maint:  $",str(Maint)])
    infoArray.append(["Other:  $",str(Other)])
    
    infoArray.append(["ListPrice:  $",str(ListPrice)])
    infoArray.append(["Sq Ft:  ",str(sqfoot)])
    infoArray.append(["Units:  ",str(TotUnits)])
    infoArray.append(["Property Tax Value: $",str(round(ReporTax/pt, 2))])
    infoArray.append(["Down Payment:  $",str(round(DownPay, 2))])
    infoArray.append(["Owner monthly expenses:  $",str(round(expO/12, 2))])
    infoArray.append(["Owner monthly expenses + mortgage:  $",str(round((expO/12) + c, 2))])
    infoArray.append(["Net monthly income:  $",str(round(((TotIn*12 - (expO + c*12))/12), 2))])
    infoArray.append(["Gross monthly income:  $",str(TotIn)])
    infoArray.append(["Yearly Net Earnings on Investment:  ",str(round((TotIn*12 - (expO + c*12))/(ListPrice*DownPP)*100, 2)) + '%'])
    infoArray.append(["Virtual Gross Earnings to Investment:  ",str(round((TotIn*12)/(ListPrice*DownPP)*100, 2)) + '%'])

    return infoArray;