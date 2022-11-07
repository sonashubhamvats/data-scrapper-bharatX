# data-scrapper-bharatX
## Requirements:
* Installing all the packages:
  * Navigate to the base directory of the project and execute:<br>
  ```pip install -r pyScript/requirements.txt```
* Installing poppler:
  * Either download the binary file or simply use choco:<br>
  ```choco install poppler``` 
* Installing the tesseract OCR:
  * This is the file which aids us in doing the NLP in this project-<br> 
  * Go to this <a href='https://drive.google.com/file/d/1251VS1n8pqwK0sEQGqHw1VlzrEVarPlE/view?usp=share_link'>link</a> and download the zip file.
  * Unzip the file in the base directory of the folder<br>
    ![image](https://user-images.githubusercontent.com/66525380/200206134-9d8ee38d-d72d-4c9f-b34a-2cd36e4e69cd.png)

## What the app uses:
* The app is built using python.
* To create the REST api we take the help of flask
* To automate the web surfing process for data scraping we use selenium 
* To bypass the captcha we either resort to manual means or an api called – “2CaptchaApi”
* Other than this for image processing and contouring we use open cv and numpy
* Most of the NLP processes like – OCR and transliteration is handled by various helper packages like – tesseract OCR , indic_transliteration etc.
## How the app works:
1.  We initialize with a GET request to the flask REST API running locally.
2.  The input information for the person to search for is provided in the body of the request.
3.	We take the input values and start our selenium bot.<br><br>
    ![image](https://user-images.githubusercontent.com/66525380/200200004-abc69023-1683-4cc4-812a-7d03db5d2a9d.png)
4.  The bot opens the site (https://electoralsearch.in/) and after putting in the details, we are redirected to yet another site where we the bot obtains assembly-constituency number and part_number from the html content.<br><br>
    ![image](https://user-images.githubusercontent.com/66525380/200200032-5af188d7-acd7-4cd7-941a-247a333321a4.png)
5.  After this we create another driver and our bot fires up again and opens up the site(https://www.nvsp.in/) through which we are redirected to the respective state electoral poll site.
6.  The state electoral site for each state is unique, with their own design and dom architecture, due to which I was only able to design the data scrapper for two state websites (UP and Madhya Pradesh).<br><br>
    ![image](https://user-images.githubusercontent.com/66525380/200200081-3aecf5b0-f959-45b9-901d-b27f6b411b6c.png)

7.  Although all the state sites are different they all require the same input and once our bot puts in those values , it starts the download for the electoralRoll pdf for that constituency.
8.  Once we have the electoral pdf we begin with the NLP side of things. I have only placed the support for Hindi<->English Language in this particular project.
9.  As the electoralRoll is a pdf file with scanned images , we need to first segregate the pdf pages into separate image data.<br><br>
    ![image](https://user-images.githubusercontent.com/66525380/200200090-467eb69b-fb4c-459f-9f62-ca40788b316d.png)
10. Once we have the image data we need to find the contours in the image to point out the cells that has our textual information.
11. Once the contouring is complete we need to do an OCR on the image , the text that we would receive in return in this case would be in Hindi.
12.	We need to first transliterate it into English and then we refine and consolidate our data.
13.	Once we have our data(name , husband/father name) regarding the people living in that area we can execute our algorithm to print the family tree of the person.
## Running the application:
•	Move to the pyScript directory(V IMP) in the project and start the program by running index.py
•	I would recommend for testing purposes to only input the following inputs into the API , as these are the tested inputs which would surely return a satisfactory       family tree.<br><br>
  For UP-<br>
  ```json
  {
    "manually_input_captcha":false,
    "name_of_the_voter":"Radhika Devi",
    "kin_name_voter":"Triloki",
    "dob_provided":false,
    "dob_voter":"18/02/1977",
    "age":"59",
    "gender_provided":"F",
    "state":"Uttar Pradesh",
    "district":"Basti",
    "assembly_const":"Kaptanganj"
  }
  ```
  For Madhya Pradesh-
  ```json
  {
    "manually_input_captcha":true,
    "name_of_the_voter":"SHYAMA",
    "kin_name_voter":"SUKHARAM",
    "dob_provided":false,
    "dob_voter":"18/02/1977",
    "age":"45",
    "gender_provided":"F",
    "state":"Madhya Pradesh",
    "district":"BALAGHAT",
    "assembly_const":"BALAGHAT"
  }
  ```
•	The "manually_input_captcha": property in the request body is set to true by default , this enables the user to input the captcha manually within 15 seconds otherwise to automate the captcha bypassing process(although it is not that accurate) set the "manually_input_captcha": as true.

## Drawbacks:
- NLP and transliteration takes the maximum amount of time as I am using an external package. Sometimes the whole process can take more than 5 min.
- The api “2CaptchaAPI” although gives the most accurate results , it is still not enough and each request takes more than 15 sec to complete.
- The NLP results are pretty inaccurate , the transliteration further decreases those accuracy levels , thus printing an accurate family tree is very difficult.
- There is no viable way for the bot to know when the download for the file has been completed due to which I am using time.sleep() in automation_bot.py which can create some problems with systems with a weak Internet speed.
## Scope For Improvement in the project:
- We can broaden the scope of the project by providing support for more indic languages and more state specific electoral sites.
- The amount of external packages used in the project makes the project very slow to run and sometimes highly inaccurate in their results , more native packages could be used.
- Further image processing on the cell snips of the electoral sheets can increase the accuracy levels in the results of our application.

## Demonstration video
- <a href=''>Video-link-1</a>
- <a href=''>Video-link-2</a>
