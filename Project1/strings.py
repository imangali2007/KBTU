simple_str = 'Hello'
double_quotes = "World"
multiline_str = """This is
a multiline
string"""

concat = simple_str + " " + double_quotes
repeat = "Hi! " * 3

text = "Python Programming"
char_first = text[0]
char_last = text[-1]
slice_part = text[0:6]
slice_step = text[::2]
reversed_text = text[::-1]

upper_text = text.upper()
lower_text = text.lower()
stripped = "  clean  ".strip()
split_text = text.split(" ")
joined = "-".join(["a", "b", "c"])

name = "121"
age = 1
f_string = f"Name: {name}, Age: {age}"

print(concat)
print(repeat)
print(slice_part, reversed_text)
print(f_string)