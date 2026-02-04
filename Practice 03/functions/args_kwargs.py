def sum_scores(*scores):
    total = 0
    for score in scores:
        total += score
    print(total)

def build_profile(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

sum_scores(10, 20, 30)
sum_scores(5, 5, 5, 5, 5)

build_profile(name="John", age=30, city="New York")
build_profile(user="admin", access="root", status="active")
