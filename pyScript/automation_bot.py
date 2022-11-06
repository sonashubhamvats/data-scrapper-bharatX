from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import sys
import time
from twocaptcha import TwoCaptcha


# to be hidden
API_KEY="2343ba7a304948ac4dd678b7ca0505cf"

#constants that are to be obtained from an api
name_of_the_voter=""
kin_name_voter=""
dob_provided=False
dob_voter=""
age=""
gender_provided=""
state=""
district=""
assembly_const=""
manually_input_captcha=False

def set_the_constants(n_v,k_v,if_dob,dob,a,
                        g_p,s,d,a_c,m_i_c):
    global name_of_the_voter
    name_of_the_voter= n_v
    global kin_name_voter
    kin_name_voter= k_v
    global dob_provided
    dob_provided= if_dob
    global dob_voter
    dob_voter= dob
    global age
    age = a
    global gender_provided
    gender_provided= g_p
    global state
    state= s
    global district
    district= d
    global assembly_const
    assembly_const= a_c
    global manually_input_captcha
    manually_input_captcha=m_i_c
def return_captcha_text():
    filename = "captcha.png"
    solver = TwoCaptcha(API_KEY)
    print("Trying a new captcha now...")
    result = solver.normal("captcha.png")
    captchaCode = result['code']
    print(captchaCode)
    return captchaCode
def getting_the_area_details(driver):
    continue_button_present=False
    try:
        continue_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "continue")))
        continue_button_present=True
    except NoSuchElementException:
        continue_button_present=False

    if continue_button_present:
        try:
            continue_button.click()
        except:
            continue_button_present=False

    # entering the name of the voter
    try:
        name_tag = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "name1")))
    except NoSuchElementException:
        driver.quit()
    name_tag.send_keys(name_of_the_voter)

    #entering the father's/husband's name
    try:
        kin_tag = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtFName")))
    except NoSuchElementException:
        driver.quit()
    kin_tag.send_keys(kin_name_voter)

    #selecting the radio button
    if dob_provided:
        try:
            rad_Dob = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "radDob")))
        except NoSuchElementException:
            driver.quit()
        rad_Dob.click()
        #selecting year of the person dob
        day,month,year=dob_voter.split('/')
        try:
            year_select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "yearList")))
        except NoSuchElementException:
            driver.quit()
        dropDownYear=Select(year_select)
        dropDownYear.select_by_value("number:"+year)

        #selecting month of the person dob
        try:
            month_select=driver.find_element(By.ID, "monthList")
            dropDownMonth=Select(month_select)
            dropDownMonth.select_by_value(month)
        except:
            driver.quit()

        #selecting day of the person dob
        try:
            day_select=driver.find_element(By.ID, "dayList")
            dropDownDay=Select(day_select)
            dropDownDay.select_by_value("number:"+day.strip("0"))
        except:
            driver.quit()
    else:
        age_select=driver.find_element(By.XPATH,'//*[@id="ageList"]')
        age_select_dropdown=Select(age_select)
        age_select_dropdown.select_by_visible_text(age)
    #selecting gender
    try:
        gender_select=driver.find_element(By.ID,"listGender")
        dropDownGender=Select(gender_select)
        dropDownGender.select_by_value(gender_provided)
    except:
        driver.quit()

    #selecting state
    try:
        state_select=driver.find_element(By.ID,"nameStateList")
        dropDownState=Select(state_select)
        dropDownState.select_by_visible_text(state)
    except:
        driver.quit()

    #selecting district and assembly
    district_select = driver.find_elements(By.ID, "namelocationList")
    try:
        time.sleep(1)
        dropDownDistrict = Select(district_select[0])
        dropDownDistrict.select_by_visible_text(district)
    except:
        driver.quit()
    try:
        time.sleep(1)
        dropDownAssembly = Select(district_select[1])
        dropDownAssembly.select_by_visible_text(assembly_const)
    except:
        driver.quit()

    #get the image ss
    view_details_xPath='//*[@id="resultsTable"]/tbody/tr/td[1]/form/input[25]'
    view_details_button=driver.find_elements(By.XPATH,view_details_xPath)
    max_tries=0
    while len(view_details_button)==0:
        max_tries+=1
        try:
            captcha_image = driver.find_element(By.ID, "captchaDetailImg")
            captcha_image.screenshot('captcha.png')
        except:
            driver.quit()
        if manually_input_captcha:
            time.sleep(15)
        else:
            c_code=return_captcha_text()
            try:
                captcha_box=driver.find_element(By.XPATH,'//*[@id="txtCaptcha"]')
                captcha_box.send_keys(c_code)
            except:
                driver.close()
        try:
            search_button=driver.find_element(By.ID,"btnDetailsSubmit")
            driver.execute_script('arguments[0].click()', search_button)
        except:
            driver.quit()
        time.sleep(2)
        view_details_button = driver.find_elements(By.XPATH, view_details_xPath)
        time.sleep(5)
        if max_tries>12:
            sys.exit("Error message")
    print("Right Captcha detected!")
    view_details_button[0].click()
    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: len(driver.window_handles) > 1)
    tabs=driver.window_handles
    driver.switch_to.window(tabs[1])
    constituency_number_tag = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ng-app"]/body/div[4]/div/div[1]/form/table/tbody/tr[11]/td[2]')))
    assemly_constituency_number_tag = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '// *[ @ id = "ng-app"] / body / div[4] / div / div[1] / form / table / tbody / tr[3] / td[2]')))
    return constituency_number_tag.text,assemly_constituency_number_tag.text
def opening_the_electoral_site(driver):
    driver.get("https://www.nvsp.in/")
    download_electoral_button=driver.find_element(By.XPATH,'//*[@id="box_wrapper"]/section[1]/section/div[2]/div/div/div[2]/div/div[2]/div[1]')
    download_electoral_button.click()
    state_select_electoral=driver.find_element(By.XPATH,'//*[@id="state_list"]')
    state_select_electoral_dropDown = Select(state_select_electoral)
    state_select_electoral_dropDown.select_by_visible_text(state)
    search_electoral_state_buttom=driver.find_element(By.XPATH,'//*[@id="btnGo"]')
    driver.execute_script('arguments[0].click()', search_electoral_state_buttom)

    wait=WebDriverWait(driver,10)
    wait.until(lambda driver:len(driver.window_handles)>1)

def open_Bihar_electoral_roll():
    print('opened electoral roll')
def open_MP_electoral_roll(p_n,a_n,driver):
    print(p_n,a_n)
    driver.switch_to.window(driver.window_handles[1])
    electoral_roll_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="aspnetForm"]/div[2]/div[4]/div[1]/div[3]/nav/ul/li[4]/ul/li[1]/a')))
    driver.execute_script('arguments[0].click()', electoral_roll_link)

    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: len(driver.window_handles) > 2)
    driver.switch_to.window(driver.window_handles[2])
    districtSelectMP = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ddlDist"]')))
    districtSelectMPDropdown=Select(districtSelectMP)
    districtSelectMPDropdown.select_by_visible_text(district)

    assemblySelectMP=WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_ddlAC"]')))
    assemblySelectMPDropdown=Select(assemblySelectMP)
    assemblySelectMPDropdown.select_by_visible_text(a_n+"-"+assembly_const)

    while 1 :
        if manually_input_captcha:
            time.sleep(15)
        else:
            captcha_image = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_imgCaptcha"]')))
            captcha_image.screenshot('captcha.png')
            txt=return_captcha_text()
            captcha_image_txt = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_txtCaptcha"]')))
            captcha_image_txt.clear()
            captcha_image_txt.send_keys(txt)
        submit_button=driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_btnCaptcha"]')
        driver.execute_script('arguments[0].click()',submit_button)
        time.sleep(4)
        try:
            tbodyMP=driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody')
            tr_cellsMP=tbodyMP.find_elements(By.TAG_NAME,'tr')[int(p_n)]
            td_a=tr_cellsMP.find_elements(By.TAG_NAME,'td')[3].find_element(
                By.TAG_NAME,'a'
            )
            driver.execute_script('arguments[0].click()', td_a)
            time.sleep(10)
            break
        except:
            print('Wrong captcha at MP')
    print('opened electoral roll')
def open_UP_electoral_roll(part_number,driver):
    driver.switch_to.window(driver.window_handles[1])
    close = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '// *[ @ id = "ctl00_head_btnClose"]')))
    driver.execute_script('arguments[0].click()', close)
    electoral_tag = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="home"]/div/div/div/div[1]/div/ul/li[2]/a')))
    driver.execute_script('arguments[0].click()', electoral_tag)

    #wait for tab to open then change focus
    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: len(driver.window_handles) > 2)
    driver.switch_to.window(driver.window_handles[2])

    #wait for the first drop down(district)
    district_tag = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_DDLDistrict"]')))
    districtDropdownUP=Select(district_tag)
    districtDropdownUP.select_by_visible_text(district)
    time.sleep(1)

    #enter a_c
    a_c=driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_DDL_AC"]')
    a_cDropdown=Select(a_c)
    a_cDropdown.select_by_visible_text(assembly_const)

    #click select button
    select=driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_Button1"]')
    driver.execute_script('arguments[0].click()', select)

    #pagenumber_tab
    page_numbers_rows=driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_ElecRollGrd"]/tbody/tr[22]/td/table/tbody/tr')
    part_number=int(part_number)
    no_of_clicks=int(part_number/200)
    index=int((part_number-no_of_clicks*200)/20)
    if no_of_clicks==0 and index>0:
        cells = page_numbers_rows.find_elements(By.TAG_NAME, 'td')
        page_table_link=cells[index].find_element(By.TAG_NAME, 'a')
        driver.execute_script('arguments[0].click()',page_table_link )
    else:
        for i in range(no_of_clicks):
            time.sleep(1)
            page_numbers_rows = driver.find_element(By.XPATH,
                                                    '//*[@id="ctl00_ContentPlaceHolder1_ElecRollGrd"]/tbody/tr[22]/td/table/tbody/tr')
            cells = page_numbers_rows.find_elements(By.TAG_NAME, 'td')
            page_table_link = cells[len(cells)-1].find_element(By.TAG_NAME, 'a')
            driver.execute_script('arguments[0].click()', page_table_link)
        time.sleep(1)
        page_numbers_rows = driver.find_element(By.XPATH,
                                                '//*[@id="ctl00_ContentPlaceHolder1_ElecRollGrd"]/tbody/tr[22]/td/table/tbody/tr')
        cells = page_numbers_rows.find_elements(By.TAG_NAME, 'td')
        page_table_link = cells[index].find_element(By.TAG_NAME, 'a')
        driver.execute_script('arguments[0].click()', page_table_link)
    tbody_element=driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_ElecRollGrd"]/tbody')
    tr_cells=tbody_element.find_elements(By.TAG_NAME,'tr')
    index_tr_cell=(part_number%20)
    td_cells=tr_cells[index_tr_cell].find_elements(By.TAG_NAME,'td')
    td_cell_a=td_cells[len(td_cells)-1].find_element(By.TAG_NAME,'a')
    driver.execute_script('arguments[0].click()', td_cell_a)

    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: len(driver.window_handles) > 3)
    driver.switch_to.window(driver.window_handles[3])


    while 1:
        if manually_input_captcha:
            time.sleep(15)
        else:
            captcha_img = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Image1"]')
            captcha_img.screenshot('captcha.png')
            txt=return_captcha_text()
            txt_box=driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_txtimgcode"]')
            txt_box.clear()
            txt_box.send_keys(txt)
        submit_button=driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_Button1"]')
        driver.execute_script('arguments[0].click()', submit_button)
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')
            alert = driver.switch_to.alert
            alert.accept()
            print("alert accepted")
        except:
            break






