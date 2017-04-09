import re


# Return list[user, command, message]
def parse_message(message):
    content = list()
    lines = message.split('\n')

    for line in lines:
        if line != '':
            matcher = re.search(".*:(.*)", line)
            content.append(matcher.group(1))

    return content


def choiceFromRange(choices):

    print("Please select one among the following:")
    for i, val in enumerate(choices):
        print(''.join([str(i+1), ". ", str(val)]))
    
    choice = raw_input("Your choice: ")
    wrong = not isInt(choice) or int(choice) < 1 or int(choice) > len(choices)
        
    while wrong:
        choice = raw_input("Wrong selection, please retry: ")
        wrong = not isInt(choice) or int(choice) < 1 or int(choice) > len(choices)
    return int(choice)
            
            
def isInt(value):
    try:
        int(value)
        return True
    except:
        return False
    
