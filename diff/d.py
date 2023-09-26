from time import sleep
import requests, os
from bs4 import BeautifulSoup
import difflib

page_url='https://www.geeksforgeeks.org/data-structures/'
page1_url = "https://www.google.com"

def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    # return data by retrieving the tag content
    return ''.join(soup.stripped_strings)

r = requests.get(page_url)
p = requests.get(page1_url)

r = remove_tags(r.content)
p = remove_tags(p.content)

# r = "\n".join(r.split("."))
# p = "\n".join(p.split("."))

with open("1.txt","w", encoding='utf-8') as one:
    one.write(r)

with open("2.txt","w", encoding='utf-8') as one:
    one.write(p)


os.system("python diff.py 1.txt 2.txt --html diff.html")
os.system("diff.html")


# # Import Module
# from bs4 import BeautifulSoup
# import requests
  
# # Website URL
# URL = 'https://www.geeksforgeeks.org/data-structures/'
  
# # Page content from Website URL
# page = requests.get(URL)
  
# # Function to remove tags
# def remove_tags(html):
  
#     # parse html content
#     soup = BeautifulSoup(html, "html.parser")
  
#     for data in soup(['style', 'script']):
#         # Remove tags
#         data.decompose()
  
#     # return data by retrieving the tag content
#     return ' '.join(soup.stripped_strings)
  
  
# # Print the extracted data
# print(remove_tags(page.content))