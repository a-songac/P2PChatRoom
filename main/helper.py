import re


# Return list[user, userMessage]
def parse_message(message):
    content = list()
    lines = message.split('\n')

    for line in lines:
        if line != '':
            matcher = re.search(".*:(.*)", line)
            content.append(matcher.group(1))

    return content

