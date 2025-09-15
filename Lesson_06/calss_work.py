# numbers = []
#
# for i in range(10):
#     value = input(f"Enter number #{i + 1}: ")
#     numbers.append(value)
#
# test_file = "example.txt"
#
# with open(test_file, "w", encoding="utf-8") as f:
#     for number in numbers:
#         f.write(number + "\n")
#
# print(f"Numbers are in the file {test_file}")

test_file = "example.txt"

with open(test_file, "w", encoding="utf-8") as file:
	for i in range(10):
		value = input(f"Enter number #{i + 1}: ")
		file.write(value + "\n")

print(f"Numbers are in the file {test_file}")

def read_file_lines(file_name):
	with open(file_name, "r", encoding="utf-8") as file:
		for line in file:
			yield line.rstrip("\n")


for line in read_file_lines(test_file):
	print(f"{line}")
