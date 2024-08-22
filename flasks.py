from selenium import webdriver
from selenium.webdriver.common.by import By
import  re, requests, os, random, zipfile, io, subprocess, pandas as pd, mysql.connector as a
from PIL import Image
from io import BytesIO
from flask import Flask, render_template, request, redirect, session, send_file, g
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'b\x8e\x9c'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pract136@gmail.com'
app.config['MAIL_PASSWORD'] = 'ulco xfmx kzqp nqdi'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


conn=a.connect(
    host="localhost",
    user="root",
    password="password123",
    database="project"
)

if conn.is_connected():
    print("CONNECTED TO MYSQL SERVER! ")
else:
    print("CONNECTED FAILED! ")

my=conn.cursor() 






@app.route('/')
def home():
     return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['Username']
        email = request.form['Email']
        password = request.form['Password']
        my.execute("SELECT * FROM credentials WHERE username = %s", (username,))
        user = my.fetchone()
        if user:
            error =  "USER ALREADY EXISTS"
            return render_template('register.html', error=error)
        else:
            my.execute("INSERT INTO credentials (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            conn.commit()
            error="!!ACCOUNT CREATED!!"
            return render_template('login.html', error=error)
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        my.execute("SELECT username from credentials")
        usernames = my.fetchall()
        my.execute("SELECT password from credentials")
        passwords = my.fetchall()
        found1 = any(username in item for item in usernames)
        found2 = any(password in item for item in passwords)
        if (found1 and found2):
            session['logged_in'] = True
            return redirect('/link')
        if(found1 and not found2):
            error = f"INVALID PASSWORD FOR USER: {username}"
            return render_template('login.html', error=error)
        if(not found1):
            error = f"USER: {username} NOT FOUND"
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        username = request.form['Username']
        session['username']= username
        my.execute("SELECT username from credentials")
        usernames = my.fetchall()
        found1 = any(username in item for item in usernames)
        if found1:
             otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
             session['user_otp']= otp
             my.execute("select email from credentials where username=%s",(username,))
             data = my.fetchall()
             user_email = data[0][0]
             msg = Message('Reset password in FauxSifter ', sender='pract136@gmail.com', recipients=[user_email]) 
             msg.body = f'Your OTP is: {otp}'
             mail.send(msg)
             error = f"OTP SENT ON REGISTERED EMAIL {user_email}!!"
             return render_template('otp.html',error=error)
        else:
             error = f"USER: {username} NOT FOUND"
             return render_template('forgot.html', error=error)
    return render_template('forgot.html')


@app.route('/otp', methods=['GET', 'POST'])
def otp():
    if request.method=='POST':
        OTP = request.form['OTP']
        user_otp= session.get('user_otp')
        if(OTP == user_otp):
            session.pop('user_otp')
            return redirect('/new')
        elif(OTP==""):
             error = "PLEASE ENTER OTP!"
             return render_template('otp.html', error=error)
        else:
            error = "WRONG OTP!"
            return render_template('otp.html', error=error)
    return render_template('otp.html')


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method=='POST':
      password = request.form['Password']
      username = session.get('username')
      my.execute("update credentials set password = %s where username = %s", (password, username))
      conn.commit()
      error = f"PASSWORD UPDATED FOR USER: {username}"
      return render_template('login.html', error=error)
    return render_template('new.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    error = "!!CONFIRM YOUR PASSWORD TO DELETE ACCOUNT PERMENANTLY!!"
    if request.method == 'POST':
        password = request.form['Password']
        my.execute("SELECT password from credentials")
        passwords = my.fetchall()
        found1 = any(password in item for item in passwords)
        if (found1):
            my.execute("DELETE FROM CREDENTIALS where password = %s", (password,))
            conn.commit()
            session.clear()
            error = "!!ACCOUNT DELETED SUCCESSFULLY!!"
            return render_template('login.html', error=error)
        else:
            error =  "!!WRONG PASSWORD!!"
            return render_template('delete.html', error=error)
    return render_template('delete.html', error=error)


@app.route('/link', methods=['GET', 'POST'])
def link():
       def scrape_amazon_product_info(url):
            driver = webdriver.Chrome()
            driver.get(url)
            
            product_name_element = driver.find_element(By.ID, "productTitle")  
            product_name = product_name_element.text.strip()

            product_photo1 = driver.find_element(By.ID, "imgTagWrapperId") 
            product_photo2 = product_photo1.find_element(By.TAG_NAME, "img")
            product_image_url = product_photo2.get_attribute("src")

            return product_name, product_image_url, driver
       

       def add_excel(product_name, product_image_url):
            response = requests.get(product_image_url)
            image_bytes = BytesIO(response.content)
            image = Image.open(image_bytes)
            image_path = 'product_image.jpg'
            image.save(image_path)
            data = {' ': [product_name]}
            df = pd.DataFrame(data)
            output_file = os.path.join("C:/Users/Admin/Desktop/PROJECT", 'product_original_reviews.xlsx')
            writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
            df.to_excel(writer, index=False, startrow=0)  
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            bold_format = workbook.add_format({'bold': True})
            worksheet.merge_range('A1:H2', product_name, bold_format)
            worksheet.merge_range('L1:N5', '')  
            worksheet.insert_image('L1', image_path, {'x_scale':  (4.5 / 16.89) * 0.75, 'y_scale': (3.54 / 13.82) * 0.75, 'x_offset': 10, 'y_offset': 10})    
            worksheet.merge_range('A15:E15', 'REVIEW', bold_format)
            worksheet.merge_range('G15:I15', 'REVIEWER', bold_format)
            worksheet.merge_range('K15:M15', 'REVIEW_DATE', bold_format)
            worksheet.write('O15', 'RATING', bold_format)
            
            return  writer


       def extract_reviews(review_data, driver):            
           reviews = driver.find_elements(By.XPATH, "//div[@data-hook='review']")
           for review in reviews:
             reviewer_name = review.find_element(By.XPATH, ".//span[@class='a-profile-name']").text
             review_date = review.find_element(By.XPATH, ".//span[@data-hook='review-date']").text
             pattern = r"\d+\s+\w+\s+\d{4}"
             match = re.search(pattern, review_date)
             review_date = match.group()
             review_text = review.find_element(By.XPATH, ".//span[@data-hook='review-body']").text
             rating = review.find_element(By.XPATH, ".//i[contains(@class, 'a-icon-star')]/span").get_attribute("innerHTML").split()[0]
             
             review_dict = {
                "Review Text": review_text,
                "Reviewer Name": reviewer_name,
                "Review Date": review_date,
                "Rating": rating
              }
             (review_data).append(review_dict)

           return review_data
       

       def check_next_page_exists(base_url, current_page_number, driver):
          next_page_number = current_page_number + 1
          page_index=base_url.rfind(str(current_page_number))
          next_page_url=base_url.replace(base_url[page_index], str(next_page_number))
          driver.get(next_page_url)
          if(driver.find_elements(By.XPATH, "//div[@data-hook='review']")):
             return True, next_page_url, next_page_number
          else:
             return False, next_page_url, next_page_number
          
       def send_multiple_files(output_files, zip_filename='extracted_reviews.zip'):
          zip_buffer = io.BytesIO()
          with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for output_file in output_files:
               with open(output_file, 'rb') as f:
                 zip_file.writestr(os.path.basename(output_file), f.read())
          zip_buffer.seek(0)
          os.remove(os.path.join('C:/Users/Admin/Desktop/PROJECT', 'product_original_reviews.xlsx'))
          os.remove(os.path.join('C:/Users/Admin/Desktop/PROJECT', 'product_detected_reviews.xlsx'))
          os.remove(os.path.join('C:/Users/Admin/Desktop/PROJECT', 'product_image.jpg'))
          return send_file(zip_buffer, as_attachment=True, download_name="extracted_reviews.zip")


       if (request.method == 'POST'):
            link = request.form['Link']
            product_name, product_image_url, driver= scrape_amazon_product_info(link)
            writer=add_excel(product_name, product_image_url)
            review_data=[]
            link = re.sub(r'(/dp/[A-Z0-9]{10}).*', r'\1/?pageNumber=1', link)
            review_url = link.replace("dp", "product-reviews")
            current_page_number = 1
            driver.get(review_url)
            review_data=extract_reviews(review_data, driver)

            while(True):
               res, review_url, current_page_number= check_next_page_exists(review_url, current_page_number, driver)
               if(res==False):
                  break
               driver.get(review_url)
               review_data=extract_reviews(review_data, driver)
               
            for review_dict in review_data:
                review_text = (review_dict["Review Text"]).replace("\n", "")
                review_dict["Review Text"] = review_text
                
            driver.quit()

            workbook = writer.book
            worksheet = writer.sheets['Sheet1']

            bold_format = workbook.add_format({'bold': True})

            for i, review in enumerate(review_data, start=17):  
               worksheet.write(i, 0, review["Review Text"], bold_format)
               worksheet.merge_range(i, 0, i, 4, None)
               worksheet.write(i, 6, review["Reviewer Name"], bold_format)
               worksheet.merge_range(i, 6, i, 8, None)
               worksheet.write(i, 10, review["Review Date"], bold_format)
               worksheet.merge_range(i, 10, i, 12, None)
               worksheet.write(i, 14, review["Rating"], bold_format)
              
            writer.close()
    
            subprocess.run(['python', 'review_detection.py'])
            output_files = ['product_original_reviews.xlsx', 'product_detected_reviews.xlsx']
            return send_multiple_files(output_files)
        
       
       elif ('logout' in request.args): 
           session.clear()

           error="LOGOUT SUCCESSFUL!"
           return render_template('login.html',error=error)
       
       elif ('logged_in' in session):
           error="!!LOGGED IN!!"
           return render_template('link.html', error=error)
       
       else:
           session.clear()
           error="SESSION EXPIRED! PLEASE LOGIN AGAIN!"
           return render_template('login.html', error=error)



       


if __name__ == '__main__':

    app.run()

