meal = int(input("How much was your meal? \n >>>"))
desert = int(input("How much desert did you take after your meal? \n >>> "))
taf = meal + desert
print(taf)

#For the drinks
pepsi = 350
fanta = 400
sprite = 300

#For the addition of taf and drink
ptaf = pepsi + taf
ftaf = fanta + taf
staf = sprite + taf

rep = input("Did you have any drink? \n 1. Yes  2. No \n >>>")
if rep == 1 or "Yes":
    min = input("What drink did you take? (Pepsi, Fanta, Sprite) \n >>>")
    if min == 'Pepsi':
        print(pepsi + taf)
    elif min == 'Fanta':
        print(fanta + taf)
    elif min == 'Sprite':
        print(sprite + taf)
    else:
        print("This drink you mentioned isn't on our list")

if min == 'Pepi':
    ttaf = ptaf 
elif min == 'Fanta':
    ttaf = ftaf
elif min == 'Sprite':
    ttaf = staf

tt = ttaf * 0.2


print("I know after visiting this place you must be very suprised, after all it is Great's resturant ")
print("Services have been offered to you by the staffs, so you are required to pay a tip of 20%")


def tip_calculator(mptt):
    tt = ttaf * 0.2
    mptt = tt + ttaf
    return f'{mptt} is the total amount of money you will pay before leaving this resturant .'
print(tip_calculator(tt + ttaf))



