import sys, os

sys.path.append("shared1/shared2")

from tool import cal

cal = cal()

print(cal.plus(cal.mul(4, 6), cal.minus(4, 6)))
