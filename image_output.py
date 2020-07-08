import imgkit


def save_image(contents, token):
	#token_start_index = contents.find(token)
	parts = contents.split(token)


	embed = "<pre style='font-size: 20px; white-space: pre-wrap; word-wrap: break-word;'>"

	tmp = ""
	for line in parts[0].splitlines(): tmp += "\n" + line
	embed += tmp[-500:].replace('<', '&lt;').replace('>', '&gt;')

	embed += token

	tmp = ""
	first = True
	for line in parts[1].splitlines(): 
		if first:
			tmp += line
			first = False

		else:
			tmp += "\n" + line

	embed += tmp[:500].replace('<', '&lt;').replace('>', '&gt;') + "\n"
	embed = embed.replace(token, "<span style='color: red'>%s</span>" % token) + "</pre>"

	imgkit.from_string(embed, 'output.jpg')