students = [
    {"name": "Alice", "grade": 88},
    {"name": "Bob", "grade": 75},
    {"name": "Charlie", "grade": 95}
]

sorted_students = sorted(students, key=lambda s: s["grade"])
print(sorted_students)

sorted_reverse = sorted(students, key=lambda s: s["grade"], reverse=True)
print(sorted_reverse)

words = ["apple", "Banana", "cherry", "Date"]
sorted_words = sorted(words, key=lambda w: w.lower())
print(sorted_words)
