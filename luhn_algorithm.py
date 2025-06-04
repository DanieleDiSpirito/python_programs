import string
import random

LEN_NUM: int = 12

def generate_number() -> str:
	# return ''.join(random.sample(string.digits, 10)) # sample() never contains duplicates
	return ''.join(random.choice(string.digits) for _ in range(LEN_NUM))

def generate_number_int() -> int:
	return int(''.join(random.choice(string.digits) for _ in range(LEN_NUM)))

def verify_number(num: str) -> bool:
	last_dig: int = int(num[-1])
	num = num[:-1]
	sec_num: list = [''] * (LEN_NUM - 1)
	for i, n in enumerate(num):
		if (i+1) % 2 == 0: # -> i % 2 != 0
			sec_num[i] = n
		else:
			number = int(n) * 2
			sum_dig: int = 0
			for dig in str(number):
				sum_dig += int(dig)
			sec_num[i] = str(sum_dig)
	sec_num_str = ''.join(sec_num)
	sum_dig: int = 0
	for dig in str(sec_num_str):
		sum_dig += int(dig)
	return 10 - sum_dig % 10 == last_dig


def analyze() -> None:
	
	not_valid: int = 0
	valid: int = 0

	while True:
		try:
			num: str = generate_number()
			if verify_number(num): valid += 1
			else:                  not_valid += 1
		except KeyboardInterrupt:
			break

	print(f'\nValid: \t\t{valid}\nNot valid: \t{not_valid}')
	print("Valid (%): \t{:.2f}\nNot valid (%):\t{:.2f}".format(
		(valid/(not_valid + valid) * 100), (not_valid/(valid + not_valid) * 100)
	))


if __name__ == '__main__':
	
	restart: bool = False
	
	while not restart:
		
		choice = input("""Select your choice:
1. Generate valid code
2. Verify code
3. Percentuage valid code
""")
		try:
			print(f"Your choice: {int(choice)}")
		except:
			print("Error found!")
			exit(1)

		choice = int(choice)
	
		restart = True
		match choice:
			case 1:
				while True:
					num: str = generate_number()
					if verify_number(num):
						print(f"Your code: {num}")
						break
				break
			case 2:
				number: str = input("Insert number: ")
				print("Valid" if verify_number(number) else "Unvalid")
				break
			case 3:
				print("Ctrl+C to stop it and see analysis")
				analyze()
				break
			case _:
				restart = False