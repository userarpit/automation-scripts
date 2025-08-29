import re

pattern = re.compile(r'(\+1-(\d{3}))?-\d{3}-\d{4}')
mo = pattern.search('My number is -456-7890.')
print(mo.group())  # Output: 123-456-7890

# mo = pattern.findall('My numbers are +1-123-456-7890 and 987-654-3210.')
# print(mo)  # Output: ['123-456-7890', '987-'