# pip install bs4

from bs4 import BeautifulSoup
from urllib.request import urlopen

# First get the link of the major you are looking for, here I'm looking for the stats and comp sci requirements
# (make sure it is the degree requirements page)
link = "http://catalog.illinois.edu/undergraduate/eng_las/statistics-computer-science-bslas/#degreerequirementstext"

# Opening the link with urlopen()
page = urlopen(link)

# Creating the html parser
soup = BeautifulSoup(page, 'html.parser')

# HTML files are structured by tags, which have opening and closing tags. Closing tags have a '/'
# tags can represents different components in a website
#
# the <p> tag is a paragraph tag where text can be put
# the <u> tag stores a lin
# the <div> tag is a grouping tag, it can use used to organize other components together
#
# tags can have attributes that add function
# for example, <u> can have the attribute 'href' to direct it to a link, so when a person presses on it they are directed to the link
#
# <u href = 'www.google.com'>Click Here!</u>
# will lead to a text 'Click Here!' that will take you to Google
# 
# if you want to test some of these features, you can go on to your browser, type in about:blank and then right click and click
# inspect element.
#
# Then you can click edit HTML in the html part and enter the tags you want
#
# An example:
# <div>
#   <p>
#       Text
#   </p>
# </div>        
#
# BeautifulSoup is a library that can extract these tags and the information stored in them
#
# Some tags have attributes called "classes" which are attributes that people assign to tags to organize them better.
# 
# for example:
#
# <div class = 'Name'>
#   <p>
#       Challen
#   </p>
# </div>   
# <div class = 'Code'>
#   <p>
#       CS124
#   </p>
# </div>   
# We can use BeautifulSoup to extract these classes
# 
#
# To learn more about HTML, I recommend this website: https://www.w3schools.com/html/default.asp
#
# Here, I am trying to get the degree requir,trements for a major
# this is a look that goes through all tags <tr> that have the class name "even" or "odd"
for block in soup.findAll('tr', attrs={'class':['even', 'odd']}):
    # I get the coruse name by finding a child tag <td> within <tr> and then extracting the second element (index 1) and gettin the text
    course_name = block.findChildren('td')[1].getText()
    # The course code is a link, so I'm going to find it by finding the <a> tag
    a_tag = block.findChild('a')
    # The number of hours is in a <td> tag with a class name of 'hourscol', so I will try to find a child tag with that attribute
    td_tag = block.findChild('td', attrs = {'class' : 'hourscol'})
    # Sometimes the <a> will not exist, so I need to account for that
    if (not a_tag is None):
        # Some <td class = 'hourscol'> do not have an hour listed next to it, so I will set a default hour of 3
        hour = 3
        # I use a try catch block in case the <td class = 'hourscol'> tag is empty (and set default hours = 3)
        try:
            hour = td_tag.getText()
            if hour == "":
                hour = 3
        except:
            hour = 3
        # Here I'm using a formatted string to print this info into the console
        print(f'{a_tag.getText()}, {course_name}, {hour}')

# Maybe there is a way to put this data into a python Dataframe? 
