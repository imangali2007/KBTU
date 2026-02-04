def calculate_damage(base_damage, multiplier):
    return base_damage * multiplier

def get_full_name(first, last):
    return f"{first} {last}"

def is_critical_hit(chance):
    return chance > 0.8

dmg = calculate_damage(50, 1.5)
print(dmg)

hero = get_full_name("Tony", "Stark")
print(hero)

crit = is_critical_hit(0.9)
print(crit)
