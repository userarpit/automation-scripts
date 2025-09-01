import re

beginswithhelloregex = re.compile(r'Hello$')
print(beginswithhelloregex.search('Hello there!Hello').group())  # Output: <