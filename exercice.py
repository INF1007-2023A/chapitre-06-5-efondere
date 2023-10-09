#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NOTE: pour exam, se souvenir des fonctions et operateurs de base, etc.
# aussi, reviser comment supprimer un element d'une liste


def check_brackets(text, brackets):
	bracket_dict = { brackets[i+1]: brackets[i] for i in range(0, len(brackets), 2) }
	opening_chars = { c for c in brackets[::2] }
	closing_chars = { c for c in brackets[1::2] }

	# pile vide
	bracket_stack = []

	# pour chaque caractere
	for c in text:
		# si le caractere est ouvrant
		if c in opening_chars:
			# empiler le caractere
			bracket_stack.append(c)
		# sinon si le caractere est fermant
		elif c in closing_chars:
			## OU: combiner la premiere et derniere condition en une pour ne pas avoir a
			# indenter le bracker_stack.pop()
			# si pile est vide
			if len(bracket_stack) == 0:
				# erreur
				return False
			# si la pile contient le caractere a fermer au bon endroit
			elif bracket_dict[c] == bracket_stack[-1]:
				# on depile
				bracket_stack.pop()
			# pas le bon caractere
			else:
				# erreur
				return False

	# succes si bracket_stack est vide, erreur sinon
	return len(bracket_stack) == 0

def remove_comments(full_text, comment_start, comment_end):
	comment_stack = []  # list containing the position of the starting commnent
	comment_pairs = [] # list of tuples containing the start and end of comment section.
	for i in range(len(full_text) - min(len(comment_start), len(comment_end)) + 1):
		if i + len(comment_start) < len(full_text) and full_text[i:i + len(comment_start)] == comment_start:
			comment_stack.append(i)
		if i + len(comment_end) < len(full_text) and full_text[i:i + len(comment_end)] == comment_end:
			if len(comment_stack) == 0:
				return None
			comment_pairs.append((comment_stack.pop(), i + len(comment_end)))
	if len(comment_stack) != 0:
		return None

	final_str = ""
	start_position = 0
	for pair in comment_pairs:
		final_str += full_text[start_position:pair[0]]
		start_position = pair[1]
	final_str += full_text[start_position:]

	return final_str

def get_tag_prefix(text, opening_tags, closing_tags):
	for tag in opening_tags:
		if text.startswith(tag):
			return (tag, None)

	for tag in closing_tags:
		if text.startswith(tag):
			return (None, tag)

	return (None, None)

def check_tags(full_text, tag_names, comment_tags):
	text = remove_comments(full_text, comment_tags[0], comment_tags[1])
	if text is None:
		return False

	opening_tags = ["<" + tag_name + ">" for tag_name in tag_names]
	closing_tags = ["</" + tag_name + ">" for tag_name in tag_names]
	tag_stack = []
	# en suivant le corrige, j'ai change la boulce suivante pour iterer sur la string caractere par
	# caractere
	while len(text) != 0:
		opening_tag, closing_tag = get_tag_prefix(text, opening_tags, closing_tags)
		if opening_tag is not None:
			tag_stack.append(opening_tag[1:-1])
			text = text[len(opening_tag):]
		elif closing_tag is not None:
			if len(tag_stack) == 0:
				return False
			if tag_stack.pop() != closing_tag[2:-1]:
				return False
			text = text[len(closing_tag):]
		else:
			# avancer d'un caractere
			text = text[1:]


	return len(tag_stack) == 0


if __name__ == "__main__":
	brackets = ("(", ")", "{", "}", "[", "]")
	yeet = "(yeet){yeet}"
	yeeet = "({yeet})"
	yeeeet = "({yeet)}"
	yeeeeet = "(yeet"
	print(check_brackets(yeet, brackets))
	print(check_brackets(yeeet, brackets))
	print(check_brackets(yeeeet, brackets))
	print(check_brackets(yeeeeet, brackets))
	print()

	spam = "Hello, world!"
	eggs = "Hello, /* OOGAH BOOGAH world!"
	parrot = "Hello, OOGAH BOOGAH*/ world!"
	dead_parrot = "Hello, /*oh brave new */world!"
	print(remove_comments(spam, "/*", "*/"))
	print(remove_comments(eggs, "/*", "*/"))
	print(remove_comments(parrot, "/*", "*/"))
	print(remove_comments(dead_parrot, "/*", "*/"))
	print()

	otags = ("<head>", "<body>", "<h1>")
	ctags = ("</head>", "</body>", "</h1>")
	print(get_tag_prefix("<body><h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("<h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("</h1></body>", otags, ctags))
	print(get_tag_prefix("</body>", otags, ctags))
	print()

	spam = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    </title>"
		"  </head>"
		"  <body>"
		"    <h1>Hello, world</h1>"
		"    <!-- Les tags vides sont ignorés -->"
		"    <br>"
		"    <h1/>"
		"  </body>"
		"</html>"
	)
	eggs = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    <!-- Il manque un end tag"
		"    </title>-->"
		"  </head>"
		"</html>"
	)
	parrot = (
		"<html>"
		"  <head>"
		"    <title>"
		"      Commentaire mal formé -->"
		"      Example"
		"    </title>"
		"  </head>"
		"</html>"
	)
	tags = ("html", "head", "title", "body", "h1")
	comment_tags = ("<!--", "-->")
	print(check_tags(spam, tags, comment_tags))
	print(check_tags(eggs, tags, comment_tags))
	print(check_tags(parrot, tags, comment_tags))
	print()

