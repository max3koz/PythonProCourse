import threading

total_words = 0
lock = threading.Lock()


def count_words(word_list):
	global total_words
	with lock:
		total_words += len(word_list)


with open('text.txt', 'r', encoding='utf-8') as f:
	text = f.read()

words = text.split()
num_threads = 4
chunk_size = len(words) // num_threads
threads = []

for i in range(num_threads):
	start = i * chunk_size
	end = len(words) if i == num_threads - 1 else (i + 1) * chunk_size
	chunk = words[start:end]
	thread = threading.Thread(target=count_words, args=(chunk,))
	threads.append(t)
	thread.start()

for thread in threads:
	thread.join()

print(f"Загальна кількість слів: {total_words}")
