import random

class Markov (object):
	
	def __init__ (self, open_file):
		self.cache = {}
		self.open_file = open_file
		self.words = self.parse()
		self.words_size = len(self.words)
		self.lines = self.parse(False,'\n')
		self.lines_size = len(self.lines)
		self.database()
		
	
	def parse (self, delete_linebreaks=True, splitchar=' '):
		self.open_file.seek(0)
		if delete_linebreaks:
			data = self.open_file.read().replace('\n',' ')
		else:
			data = self.open_file.read()
		words = data.split(splitchar)
		return words
		
	
	def triples (self):
		""" Generates triples from the given data string. So if our string were
				"What a lovely day", we'd generate (What, a, lovely) and then
				(a, lovely, day).
		"""
		
		if len(self.words)<3:
			return
		
		for i in range(len(self.words)-2):
			yield (self.words[i], self.words[i+1], self.words[i+2])
			
	def database (self):
		for w1, w2, w3 in self.triples():
			key = (w1, w2)
			if key in self.cache:
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]
				
	def generate_markov_text (self):
		seed = random.randint(0,self.lines_size-2)
		w1, w2 = '<title>', self.lines[seed].split(' ')[1]
		gen_words = []
		while w1 != "</title>":
			gen_words.append(w1)
			w1, w2 = w2, random.choice(self.cache[(w1, w2)])
		gen_words.pop(0)
		return ' '.join(gen_words)