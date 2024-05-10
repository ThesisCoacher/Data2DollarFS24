from bs4 import BeautifulSoup
import re

# Open the HTML file and read its content
with open('your_file.html', 'r') as f:
    content = f.read()

# Parse the HTML content
soup = BeautifulSoup(content, 'html.parser')

# Find all the elements with the attribute `href`
elements = soup.find_all(href=True)

# Define the pattern for the links
pattern = r'^https://www\.musement\.com/us/new-york/.+-\d{4,6}/$'

# Extract the `href` attribute from these elements and check if it matches the pattern
links = [element.get('href') for element in elements if re.match(pattern, element.get('href'))]

# Remove 'None' elements
links = [link for link in links if link is not None]
# Print the list
print(links)
print(len(links))