import re

pattern = re.compile(r'''(\+1-  # country code
                     (\d{3}))?-   # area code
                     \d{3}-\d{4}''', re.VERBOSE)

mo = pattern.search('My number is +1-234-456-7890.')
print(mo.group())  # Output: 123-456-7890

# mo = pattern.findall('My numbers are +1-123-456-7890 and 987-654-3210.')
# print(mo)  # Output: ['123-456-7890', '987-'