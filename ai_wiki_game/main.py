import requests
import bs4
from sys import argv
import re
from sys import stdout
from os.path import expanduser
from time import perf_counter
from functools import lru_cache
import pickle

class IllegalArgumentError(ValueError):
    pass

USE_PICKLE = True


@lru_cache()
def cosine_sim(title1, title2):
	avg_v1 = get_word_embedding(title1)
	avg_v2 = get_word_embedding(title2)
	if avg_v1 is None:
		return float('inf')
	return 1 - model.cosine_similarities(avg_v1, [avg_v2])[0]

def is_dest_embedding_possible(title):
	words = title.split("_")
	for word in words:
		if word in model:
			return True
		elif word.lower() in model:
			return True
	return False

def get_word_embedding(phrase):
	words = phrase.split("_")
	sum_v = [0.0] * model.vector_size
	n_words = 0
	for word in words:
		if word in model:
			sum_v += model.get_vector(word)
			n_words += 1
		elif word.lower() in model:
			sum_v += model.get_vector(word.lower())
			n_words += 1
	if n_words == 0:
		return None
	avg_v = sum_v / n_words
	return avg_v


if __name__ == '__main__':

	''' CHECKING ARGUMENTS '''
	if len(argv) != 3:
		raise IllegalArgumentError("Usage: main.py <origin> <destination>")
	origin_link, dest_link = argv[1:3]
	if re.match(r"https://[a-z]{2}.wikipedia.org/wiki/", origin_link) is None:
		raise IllegalArgumentError("Origin link is not a Wikipedia link! Valid wiki link example: https://<language>.wikipedia.org/wiki/<title>")
	if re.match(r"https://[a-z]{2}.wikipedia.org/wiki/", dest_link) is None:
		raise IllegalArgumentError("Destination link is not a Wikipedia link! Valid wiki link example: https://<language>.wikipedia.org/wiki/<title>")
	origin_title = origin_link.split("/wiki/")[1]
	dest_title = dest_link.split("/wiki/")[1]
	lang = origin_link.split("/")[2].split(".")[0]
	if lang != dest_link.split("/")[2].split(".")[0]:
		raise IllegalArgumentError("Origin and destination links must be in the same language Wikipedia!")
	print(f"GAME SETTINGS ⚙️\nOrigin: {origin_link}\nDestination: {dest_link}\nLanguage: {lang}\n" + "-"*152)
	session = requests.Session()
	session.headers.update({
		"User-Agent": "MyPythonWikipediaClient/1.0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	})
	origin_page = session.get(origin_link)
	if origin_page.status_code != 200:
		raise IllegalArgumentError("Origin page does not exist!")
	dest_page = session.get(dest_link)
	if dest_page.status_code != 200:
		raise IllegalArgumentError("Destination page does not exist!")
	
	
	''' LOAD MODEL '''
	model_loaded = False
	stdout.write("⏳ Loading word2vec-google-news-300 model... ")
	stdout.flush()
	if USE_PICKLE:
		try:
			with open('word2vec-google-news-300.pkl', 'rb') as f:
				model = pickle.load(f)
			model_loaded = True
		except Exception:
			stdout.write('\nNo pickle found, loading model normally...')
			stdout.flush()
			pass
	if not model_loaded:
		from gensim.models import KeyedVectors
		import gensim.downloader as api
		try:
			model = KeyedVectors.load_word2vec_format(expanduser("~/gensim-data/word2vec-google-news-300/word2vec-google-news-300.gz"), binary=True)
			if USE_PICKLE:
				with open('word2vec-google-news-300.pkl', 'wb') as f:
					pickle.dump(model, f)
				model_loaded = True
				print('Model pickled for faster loading next time.')
		except Exception as e:
			stdout.write(f"\nError loading model: {e}\n")
			stdout.flush()
			model = api.load('word2vec-google-news-300')
	stdout.write("Model loaded successfully. ✅\n")
	stdout.flush()

	if not is_dest_embedding_possible(dest_title):
		raise IllegalArgumentError("Destination page title has no valid word embeddings in the model! Cannot compute similarity.")


	''' STARTING GAME '''
	num_links = 1
	history = [origin_title]
	min_distance = cosine_sim(origin_title, dest_title)
	distances = [min_distance]
	found = False
	curr_link = origin_link
	starting_time = perf_counter()
	visited_links = set()
	visited_links.add(origin_link)
	while not found:
		print(f"CURRENT PAGE: {curr_link:100}\tDistance to target: {min_distance:.10f}")
		curr_page = session.get(curr_link)
		soup = bs4.BeautifulSoup(curr_page.text, 'html.parser')
		links = soup.find_all('a', href=True) # get every link in <a>
		found = False
		min_distance = float('inf')
		next_link = None
		for link in links:
			href = link['href']
			if href.startswith("/wiki/") and ':' not in href:
				full_link = f"https://{lang}.wikipedia.org{href}"
				if full_link in visited_links:
					continue
				if full_link == dest_link:
					history.append(dest_title)
					distances.append(0.0)
					print(f"CURRENT PAGE: {full_link:100}\tDistance to target: {0.0:.10f}\n" + "-"*152)
					ending_time = perf_counter()
					found = True
					break
				curr_title = href.split("/wiki/")[1]
				distance = cosine_sim(curr_title, dest_title)
				if distance < min_distance:
					min_distance = distance
					next_link = full_link
		else:
			if next_link is None:
				raise Exception("No valid links found on the page! 💀")
			history.append(next_link.split("/wiki/")[1])
			visited_links.add(next_link)
			distances.append(min_distance)
			num_links += 1
			curr_link = next_link
	print("\n\nAI WINS! 🎉")
	print(f"Number of links traversed: {num_links}")
	print(f"Total time taken: {ending_time - starting_time:.3f} seconds")
	
