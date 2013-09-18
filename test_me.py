
from CalCalc import calculate

def test_1(): 
	assert calculate("3 + 7") == 11

def test_2():
	assert abs(calculate("5.0**3.0 - 125.0")) < 10**(-12)

def test_3():
	assert abs(calculate("Mass of the proton in grams") - 1.672622*10**(-24)) < 10**(-5)

def test_4():
	assert "42" in calculate("What is the meaning of life?")

def test_5():
	assert abs(calculate("e^(sqrt(-1)*2pi)") - 1.0) < 10**(-12)