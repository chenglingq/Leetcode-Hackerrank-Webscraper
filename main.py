import json
import pickle
import time

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


# Get upto which problem it is already scraped from track.conf file
completed_upto = read_tracker("track.conf")

# Load chapters list that stores chapter info
# Store chapter info
with open('chapters.pickle', 'rb') as f:
    chapters = pickle.load(f)

def download(problem_num, url, title, solution_slug, frontend_question_id):  
    print(Fore.BLACK + Back.CYAN + f"Fetching problem num " + Back.YELLOW + f" {problem_num} " + Back.CYAN + " with url " + Back.YELLOW + f" {url} ")
    n = len(title)

    try:
        with open('solution_content_10_30.txt','a', encoding ='utf-8') as fd:
            fd.write( "\nPROBNUM:"+str(frontend_question_id)+"\n")

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
        title_decorator = '*' * n
        problem_title_html = title_decorator + f'<div id="title">{title}</div>' + '\n' + title_decorator
        problem_html = problem_title_html + str(soup.find("div", {"class": "content__QRGW"})) + '<br><br><hr><br>'
        #problem_html2 = problem_title_html + str(soup.find_all("div", {"class": re.compile("css\+[a-zA-Z0-9_]e5i1odf0")})) #+ '<br><br><hr><br>'
        #<div class="css-blecvm e5i1odf0">
        #<div class="css-16xmbhl e5i1odf0">
        with open('solution_content_10_30.txt','a', encoding ='utf-8') as fd:
            #fd.write( "\nPROBNUM:"+str(frontend_question_id)+"\n")
            fd.write(str(soup.find("div", {"class": "content__QRGW"}).get_text('')).replace(u'\xa0', u''))
            fd.write('\nENDOFPROB\n')

################


        # Append Contents to a HTML file

        with open("content_out.html", "ab") as f:
            f.write(problem_html.encode(encoding="utf-8"))


        # create and append chapters to construct an epub


        # Write List of chapters to pickle file
        # Update upto which the problem is downloaded
        update_tracker('track.conf', problem_num)
        print(Fore.BLACK + Back.GREEN + f"Writing problem num " + Back.YELLOW + f" {problem_num} " + Back.GREEN + " with url " + Back.YELLOW + f" {url} " )
        print(Fore.BLACK + Back.GREEN + " successfull ")
        # print(f"Writing problem num {problem_num} with url {url} successfull")

    except Exception as e:
        print(Back.RED + f" Failed Writing!!  {e} ")
        with open('solution_content_10_30.txt','a', encoding ='utf-8') as fd:       
            fd.write('\nENDOFPROB\n') 
        #driver.quit()

def main():

    # Leetcode API URL to get json of problems on algorithms categories
    ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"

    # Problem URL is of format ALGORITHMS_BASE_URL + question__title_slug
    # If question__title_slug = "two-sum" then URL is https://leetcode.com/problems/two-sum
    ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"
    
    # solution suffix
    SOLUTION_END = "/solution/"

    # Load JSON from API
    algorithms_problems_json = requests.get(ALGORITHMS_ENDPOINT_URL).content
    algorithms_problems_json = json.loads(algorithms_problems_json)

    styles_str = "<style>pre{white-space:pre-wrap;background:#f7f9fa;padding:10px 15px;color:#263238;line-height:1.6;font-size:13px;border-radius:3px margin-top: 0;margin-bottom:1em;overflow:auto}b,strong{font-weight:bolder}#title{font-size:16px;color:#212121;font-weight:600;margin-bottom:10px}hr{height:10px;border:0;box-shadow:0 10px 10px -10px #8c8b8b inset}</style>"
    with open("out.html", "ab") as f:
            f.write(styles_str.encode(encoding="utf-8"))


    print("The user name is :" + str(algorithms_problems_json["user_name"])+".\n")
    # List to store question_title_slug
    links = []
    for child in algorithms_problems_json["stat_status_pairs"]:
            # Only process free problems
            #if not child["paid_only"]:
        question__title_slug = child["stat"]["question__title_slug"]
        question__article__slug = child["stat"]["question__article__slug"]
        question__title = child["stat"]["question__title"]
        frontend_question_id = child["stat"]["frontend_question_id"]
        difficulty = child["difficulty"]["level"]

        links.append((question__title_slug, difficulty, frontend_question_id, question__title, question__article__slug))

    # Sort by difficulty follwed by problem id in ascending order
    #links = sorted(links, key=lambda x: (x[1], x[2]))
    links = sorted(links, key=lambda x: x[2])

    textfile = open("a_file.txt", "w")
    for element in links:
        textfile.write(str(element))
        textfile.write("\n")
    textfile.close()

    print("The length of links is :"+ str(len(links))+".\n")

    try: 
        for i in range(completed_upto + 1, len(links)):
             question__title_slug, _ , frontend_question_id, question__title, question__article__slug = links[i]
             url = ALGORITHMS_BASE_URL + question__title_slug + SOLUTION_END
             title = f"{frontend_question_id}. {question__title}"

             # Download each file as html and write chapter to chapters.pickle
             download(i, url , title, question__article__slug, frontend_question_id)

             # Sleep for 20 secs for each problem and 2 minns after every 30 problems
             if i % 30 == 0:
                 print(f"Sleeping 60 secs\n")
                 time.sleep(60)
             else:
                 print(f"Sleeping 10 secs\n")
                 time.sleep(10)

    finally:
        # Close the browser after download
        driver.quit()
    
    try:
        epub_writer.write("Leetcode Questions.epub", "Leetcode Questions", "Anonymous", chapters)
        print(Back.GREEN + "All operations successful")
    except Exception as e:
        print(Back.RED + f"Error making epub {e}")
    


if __name__ == "__main__":
    main()
