import time
import math

def multiply_list(nums):
    return math.prod(nums)

def count_case(s):
    upper = sum(1 for c in s if c.isupper())
    lower = sum(1 for c in s if c.islower())
    return upper, lower

def is_palindrome(s):
    return s == s[::-1]

def delayed_sqrt(n, ms):
    time.sleep(ms / 1000)
    print(f"Square root of {n} after {ms} miliseconds is {math.sqrt(n)}")

def all_true(t):
    return all(t)

print(multiply_list([1, 2, 3, 4]))
print(count_case("Hello World"))
print(is_palindrome("madam"))
# delayed_sqrt(25100, 2123)
print(all_true((True, 1, "test")))
