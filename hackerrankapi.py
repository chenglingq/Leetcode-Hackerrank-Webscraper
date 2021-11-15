import json
import pickle
import time
import re
import bs4
import colorama
import requests
from colorama import Back, Fore
from ebooklib import epub
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils import *
import epub_writer

# Initialize Colorama
colorama.init(autoreset=True)

# Setup Selenium Webdriver
CHROMEDRIVER_PATH = r"C:/Users/cheng/cs329p/leetcode/chromedriver.exe"
options = Options()
options.add_argument(r"--user-data-dir=C:\\Users\\cheng\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument(r"--profile-directory=Profile 2")

options.headless = False
# Disable Warning, Error and Info logs
# Show only fatal errors
options.add_argument("--log-level=3")
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)

completed_upto = read_tracker("track2.conf")

with open('hacerrank_list.txt', 'r') as file :
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    #print(len(lines))

tagset = {'Warmup', 'Implementation', 'Strings','Sorting', 'Search', 'Graph Theory', 'Greedy',
          'Dynamic Programming', 'Constructive Algorithms', 'Bit Manipulation', 'Recursion',
          'Game Theory', 'NP Complete', 'Debugging','Arrays','Linked Lists', 'Trees','Balanced Trees',
          'Stacks', 'Queues', 'Heap', 'Disjoint Set', 'Multiple Choice', 'Trie', 'Advanced'
        }

# Replace the target string
#filedata = filedata.replace('?isFullScreen=true', '/problem')

# Write the file out again
# with open('hacerrank_list.txt', 'w') as file:
#   file.write(filedata)
def main():
    with open('hacerrank_list.txt', 'r') as file :
      lines = file.readlines()
      lines = [line.rstrip() for line in lines]
    print(len(lines))
    
    
    try: 
        for i in range(completed_upto + 1, len(lines)):

             #question__title_slug, _ , frontend_question_id, question__title, question__article__slug = lines[i]
             url = lines[i]
             #title = f"{frontend_question_id}. {question__title}"
             print(url)
             # Download each file as html and write chapter to chapters.pickle
             download(i, url )

             # Sleep for 20 secs for each problem and 2 minns after every 30 problems
             if i % 30 == 4:
                 print(f"Sleeping 60 secs\n")
                 time.sleep(60)
             else:
                 print(f"Sleeping 10 secs\n")
                 time.sleep(10)
    except Exception as e:
        print(Back.RED + f" Failed Writing!!  {e} ")                 

    #finally:
        # Close the browser after download
        #driver.quit()
  
def download(problem_num, url):
  print(Fore.BLACK + Back.CYAN + f"Fetching problem num " + Back.YELLOW + f" {problem_num} " + Back.CYAN + " with url " + Back.YELLOW + f" {url} ")


  try:

        

    driver.get(url)
    # Wait 20 secs or until div with id initial-loading disappears
    element = WebDriverWait(driver, 20).until(
        EC.invisibility_of_element_located((By.ID, "initial-loading"))
    )

    # Get current tab page source
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, "html.parser")

      # <a class="topic-tag__1jni" href="/tag/string/"><span data-size="xs" class="tag__24Rd">String</span></a>
    # Construct HTML

    # problem_title_html = title_decorator + f'<div id="title">{title}</div>' + '\n' + title_decorator
    # problem_html = problem_title_html + str(soup.find("div", {"class": "content__QRGW"})) + '<br><br><hr><br>'
    #problem_html2 = problem_title_html + str(soup.find_all("div", {"class": re.compile("css\+[a-zA-Z0-9_]e5i1odf0")})) #+ '<br><br><hr><br>'
    #<div class="css-blecvm e5i1odf0">
    #<div class="css-16xmbhl e5i1odf0">
    title = "TITLE: "
    if soup.find("h1", {"class": "ui-icon-label page-label"}) is not None:
      title += str(soup.find("h1", {"class": "ui-icon-label page-label"}).get_text('')).replace(u'\xa0', u'') 
    difficulty = "DIFFICULTY: " 
    if soup.select('p[class*="pull-right difficulty-"]') is not None:
      difficulty += str( soup.select('p[class*="pull-right difficulty-"]')[0].get_text())
    tag = "TAG: "
    for data in soup(['style']):
        # Remove tags
        data.decompose()
    content = "CONTENT: "    
    if soup.find("div", {"class": "challenge_problem_statement"}) is not None:
      content += str(soup.find("div", {"class": "challenge_problem_statement"}).get_text('')).replace(u'\xa0', u'')  
    input_format = "INPUTFORMAT: "
    if soup.find(True, {'class':["challenge_input_format", "challenge_sample_input"]}) is not None:
    #input_format = "INPUTFORMAT: " + str(soup.find("div", {"class": "challenge_input_format"}).get_text('')).replace(u'\xa0', u'')+" ENDOFINPUTFORMAT"
      input_format += str(soup.find(True, {'class':["challenge_input_format", "challenge_sample_input"]}).get_text('')).replace(u'\xa0', u'')
    constraints = "CONSTRAINTS: "
    if soup.find("div", {"class": "challenge_constraints"}) is not None:
      constraints += str(soup.find("div", {"class": "challenge_constraints"}).get_text('')).replace(u'\xa0', u'')
    #output_format = "OUTPUTFORMAT: " + str(soup.find("div", {"class": "challenge_output_format"}).get_text('')).replace(u'\xa0', u'')+" ENDOFOUTPUTFORMAT"
    output_format = "OUTPUTFORMAT: "
    if soup.find(True, {'class':["challenge_output_format", "challenge_sample_output"]}) is not None:
      output_format += str(soup.find(True, {'class':["challenge_output_format", "challenge_sample_output"]}).get_text('')).replace(u'\xa0', u'')
        
    explanation = "EXPLANATION: "
    if soup.find("div", {"class": "challenge_explanation"}) is not None:
      explanation += str(soup.find("div", {"class": "challenge_explanation"}).get_text('')).replace(u'\xa0', u'')
    #content = "CONTENT: " + str(soup.find("div", {"class": "challenge-body-html"}).get_text('')).replace(u'\xa0', u'') +" ENDOFCONTENT"
    # print(title)
    # print(difficulty)
    # print(content)
    # print(input_format)
    # print(constraints)
    # print(output_format)
    # print(explanation)
    for EachPart in soup.select('span[class*="breadcrumb-item-text"]'):
      #print (EachPart.get_text())
      if EachPart.get_text() in tagset:
        tag += EachPart.get_text()
    

    #tag = "TAG: " + tag
    #print(difficulty)
    #print(tag)
    with open('hackerrank_11_11.txt','a', encoding ='utf-8') as fd:
      #fd.write( "\nPROBNUM:"+str(frontend_question_id)+"\n")
      fd.write( "\nPROBNUM:"+str(problem_num)+" ENDOFPROBNUM\n")
      fd.write(title +' ENDOFTITTLE\n')
      fd.write(difficulty+' ENDOFDIFFICULTY\n')
      fd.write(tag+' ENDOFTAG\n')
      fd.write(content+' ENDOFCONTENT\n')
      fd.write(input_format +' ENDOFINPUTFORMAT\n')
      fd.write(constraints+'  ENDOFCONSTRAINTS\n')
      fd.write(output_format+' ENDOFOUTPUTFORMAT\n')
      fd.write(explanation+'  ENDOFEXPLANATION\n')            
      fd.write('\nENDOFPROB\n')
#<span itemprop="name" class="breadcrumb-item-text">Warmup</span>
################


        # Append Contents to a HTML file

        # with open("content_out.html", "ab") as f:
        #     f.write(problem_html.encode(encoding="utf-8"))


        # create and append chapters to construct an epub


        # Write List of chapters to pickle file
        # Update upto which the problem is downloaded
    update_tracker('track2.conf', problem_num)
    print(Fore.BLACK + Back.GREEN + f"Writing problem num " + Back.YELLOW + f" {problem_num} " + Back.GREEN + " with url " + Back.YELLOW + f" {url} " )
    print(Fore.BLACK + Back.GREEN + " successfull ")
    # print(f"Writing problem num {problem_num} with url {url} successfull")

  except Exception as e:
    print(Back.RED + f" Failed Writing!!  {e} ")
    try:
      driver.get(url)
      # Wait 20 secs or until div with id initial-loading disappears
      element = WebDriverWait(driver, 20).until(
          EC.invisibility_of_element_located((By.ID, "initial-loading"))
      )

      # Get current tab page source
      html = driver.page_source
      soup = bs4.BeautifulSoup(html, "html.parser")

        # <a class="topic-tag__1jni" href="/tag/string/"><span data-size="xs" class="tag__24Rd">String</span></a>
      # Construct HTML

      # problem_title_html = title_decorator + f'<div id="title">{title}</div>' + '\n' + title_decorator
      # problem_html = problem_title_html + str(soup.find("div", {"class": "content__QRGW"})) + '<br><br><hr><br>'
      #problem_html2 = problem_title_html + str(soup.find_all("div", {"class": re.compile("css\+[a-zA-Z0-9_]e5i1odf0")})) #+ '<br><br><hr><br>'
      #<div class="css-blecvm e5i1odf0">
      #<div class="css-16xmbhl e5i1odf0">
      title = "TITLE: " + str(soup.find("h1", {"class": "ui-icon-label page-label"}).get_text('')).replace(u'\xa0', u'') 
      difficulty = "DIFFICULTY: " + str( soup.select('p[class*="pull-right difficulty-"]')[0].get_text())
      tag = "TAG: "
      for data in soup(['style']):
          # Remove tags
          data.decompose()
      content = "CONTENT: " + str(soup.find("div", {"class": "hackdown-content"}).get_text('')).replace(u'\xa0', u'') +" ENDOFCONTENT"
      
      # print(title)
      # print(difficulty)
      # print(content)
      # print(input_format)
      # print(constraints)
      # print(output_format)
      # print(explanation)
      for EachPart in soup.select('span[class*="breadcrumb-item-text"]'):
        #print (EachPart.get_text())
        if EachPart.get_text() in tagset:
          tag += EachPart.get_text()
      

      #tag = "TAG: " + tag
      #print(difficulty)
      #print(tag)
      with open('hackerrank_11_11.txt','a', encoding ='utf-8') as fd:
        #fd.write( "\nPROBNUM:"+str(frontend_question_id)+"\n")
        fd.write( "\nPROBNUM:"+str(problem_num)+" ENDOFPROBNUM\n")
        fd.write(title +' ENDOFTITTLE\n')
        fd.write(difficulty+' ENDOFDIFFICULTY\n')
        fd.write(tag+' ENDOFTAG\n')
        fd.write(content+'\n')
        # fd.write(input_format +'\n')
        # fd.write(constraints+'\n')
        # fd.write(output_format+'\n')
        # fd.write(explanation+'\n')            
        fd.write('\nENDOFPROB\n')    
      #with open('hackerrank_11_11.txt','a', encoding ='utf-8') as fd:       
          #fd.write('\nENDOFPROB\n')     
      #with open('missied_num.txt','a', encoding ='utf-8') as fd:       
        #fd.write(str(problem_num)+', ') 
    #driver.quit()
    except Exception as e:
      print(Back.RED + f" Failed Writing!!  {e} ")

if __name__ == "__main__":
    main()
