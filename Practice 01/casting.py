number_str = "1"
float_str = "3.14"
integer_val = 1
float_val = 9.1
numbers_srt = "1 2 3 4 5"

print(int(number_str))
print(int(float_val))
print(float(integer_val))
print(str(integer_val))
print(list(map(int, numbers_srt.split())))
