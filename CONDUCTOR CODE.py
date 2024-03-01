Sobo = 300
Ipaja = 140
Oshodi = 400
Ikotun = 250

print("1. Sobo")
print("2. ipaja")
print("3. Oshodi")
print("4. Ikotun")
print("Pls, where would you like to go to")

reply = (str(input))

fare =(input("How much are you wiht"))
if reply == "1" or "sobo" or "2" or "ipaja" or "3" or "Oshodi" or "4" or "Ikotun":
    print("How much are you with ?")
    if fare > 350:
       print("I don't have change")
    else:
        print("Bye, Bye")



