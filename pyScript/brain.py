import automation_bot
import operation
from selenium import webdriver
from difflib import SequenceMatcher
from selenium.webdriver.chrome.service import Service as ChromeService
import os
#check the similarity
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#initial driver for getting the assembly no
def get_area_details():
    print("Getting the constituency_number and assembly no - ")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    service = ChromeService(executable_path='../chromedriver.exe')
    driver = webdriver.Chrome(options=options,service=service)
    driver.get("https://www.electoralsearch.in/")
    constituency_number,assembly_number=automation_bot.getting_the_area_details(driver)
    driver.quit()
    print("Got the constituency_number and assembly no - ")
    return constituency_number,assembly_number

#function for extracting details from different sites
def extract_details(constituency_number,assembly_number,state):
    print("Getting data from separate state sites")
    assembly_number=assembly_number.split(' ')[-1]
    options = webdriver.ChromeOptions()
    path = os.getcwd()

    newpath = r'../testElectoralRoll' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    parent_dir = os.path.abspath(os.path.join(path, os.pardir))
    dir = [x[0] for x in os.walk(parent_dir)]
    options.add_experimental_option('prefs', {
    "download.default_directory": str(dir[len(dir)-1]), #Change default directory for downloads
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
    })
    service = ChromeService(executable_path='../chromedriver.exe')
    driver = webdriver.Chrome(options=options, service=service)
    # driver = webdriver.Chrome(service=s)
    automation_bot.opening_the_electoral_site(driver)
    if state=='Bihar':
        automation_bot.open_Bihar_electoral_roll()
    elif state=='Madhya Pradesh':
        automation_bot.open_MP_electoral_roll(constituency_number,assembly_number,driver)
    elif state=='Uttar Pradesh':
        automation_bot.open_UP_electoral_roll(constituency_number,driver)
    print("Got data from separate state sites")

#extract the dataset
def extract_larger_dataset(name_of_the_voter,kin_name_voter,dob_provided,dob_voter,age,gender_provided,state
                  ,district,assembly_const,manually_input_captcha):
    #setting the constants
    automation_bot.set_the_constants(name_of_the_voter,kin_name_voter,dob_provided,dob_voter,age,gender_provided,state
                      ,district,assembly_const,manually_input_captcha)

    #call get_area_details
    constituency_number,assembly_number=get_area_details()

    #call extract details
    extract_details(constituency_number,assembly_number,state)
    print("Larger File extracted!")

#extract data from the dataset
def extract_data_from_larger_dataset():
    return operation.get_info_about_all()

#return family tree
def get_dic(name,relation):
    return {'name':name,'relation':relation}
def get_family_details(details,electoral_dic):
    family_tree=[]
    kin_relation_key = list(details)[1]
    family_tree.append(get_dic(details['name'], 'self'))
    kin_relation = kin_relation_key.split('-')[0]
    relation=[]
    if kin_relation == "father":
        #getting father name
        father_name=details[kin_relation_key]
        #adding father to the tree
        family_tree.append(get_dic(father_name,'father'))
        #check for other relatives
        for data in electoral_dic:
            # check for siblings
            if data.get('father-name')!=None and data.get('name') != None and similar(data['name'],details['name'])<0.5:
                if similar(father_name,data['father-name'])>0.9:
                    family_tree.append(get_dic(data['name'],"sibling"))
            # check for mother
            if data.get('husband-name')!=None and data.get('name') != None:
                if similar(father_name,data['husband-name'])>0.9:
                    family_tree.append(get_dic(data['name'],'mother'))
            # check for grand parent
            if data.get('name') != None:
                if similar(father_name,data['name'])>0.9:
                    if data.get('father-name')!=None :
                        family_tree.append(get_dic(data['father-name'],'grandparent'))
    else:
        # getting husband name
        husband_name = details[kin_relation_key]
        # adding father to the tree
        family_tree.append(get_dic(husband_name, 'husband'))
        # check for other relatives
        for data in electoral_dic:
            # check for children
            if data.get('father-name')!=None :
                if similar(husband_name, data['father-name']) > 0.9:
                    family_tree.append(get_dic(data['name'], "child"))
            # check for parent in law
            if data.get('name') != None:
                if similar(husband_name, data['name']) > 0.9:
                    if data.get('father-name')!=None :
                        family_tree.append(get_dic(data['father-name'], 'parent-in-law'))
    return family_tree
def return_family_tree(name,electoral_dic):
    name=name.lower()
    details={}
    for data in electoral_dic:
        if data.get('name') != None:
            if similar(name,data['name'])>0.9:
                print('hit')
                details=data
                break
    if len(details)>1:
        ans=[]
        print(details)
        ans.append(get_family_details(details,electoral_dic))
        return ans
    else:
        # if the match is not direct
        ans=[]
        details=[]
        for data in electoral_dic:
            if data.get('name') != None:
                if similar(name, data['name']) > 0.5:
                    print('hit relative')
                    print(data)
                    details.append(data)
                    if len(details)>1:
                        break
        for detail in details:
            ans.append(get_family_details(detail, electoral_dic))
        return ans
