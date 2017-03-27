

# Return list[user, userMessage]
def parse_message(message):
	content = list()
    lines = data.split('\\n')
    matcher = re.search("b'(\w+)\s(\/\w*[\/\w]*(\.\w+)*)", lines[0])
    content.append(matcher.group(1))
    content.append(matcher.group(2))

    return content