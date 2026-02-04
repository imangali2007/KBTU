import re

with open('../row.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print("--- Products and Prices ---")
item_pattern = r"(?P<item>.*?)\n(?P<count>[\d,]+)\s+x\s+(?P<price>[\d\s,]+)\n(?P<total>[\d\s,]+)"
matches = re.finditer(item_pattern, text)

for match in matches:
    print(f"{match.group('item').strip()}: {match.group('price').strip()}")

print("\n--- Total ---")
total_pattern = r"ИТОГО:\n(?P<total>[\d\s,]+)"
total_match = re.search(total_pattern, text)
print(total_match.group("total").strip() if total_match else "Not found")

print("\n--- Date and Time ---")
time_pattern = r"Время:\s+(?P<time>[\d\.:\s]+)"
time_match = re.search(time_pattern, text)
print(time_match.group("time").strip() if time_match else "Not found")

print("\n--- Address ---")
addr_pattern = r"г\.\s+.*"
addr_match = re.search(addr_pattern, text)
print(addr_match.group(0).strip() if addr_match else "Not found")
