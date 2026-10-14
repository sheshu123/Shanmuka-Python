#IF-ELSE CONDITION

# RAMA_HEIGHT=1.3
# RAJA_HEIGHT=1.7
# if RAMA_HEIGHT > RAJA_HEIGHT:
#     print("RAMA IS TALLER")
# else:
#     print("RAJA IS TALLER")

total=float(input("Enter total purchase amount:"))
if total>=1000:
    discount=total*0.10
    final_amount=total-discount
    print("Discount applied:",discount)
    print("Final amount to pay:",final_amount)
else:
    print("No discount applied")
    print("Final amount to pay:",total)
