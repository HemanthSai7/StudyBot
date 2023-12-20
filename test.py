# class A:
#     def __init__(self):
#         self._bill = 1

#     @property
#     def bill(self):
#         return self._bill

#     @bill.setter
#     def bill(self,value):
#         self._bill = value
#         # raise PermissionError("You can't change the bill")

# class B(A):
#     def __init__(self):
#         super().__init__()
#         self._bill = 2

# # b = B()
# # print(b.bill)
# a=A()
# a.bill=3
# print(a.bill)