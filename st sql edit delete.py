import streamlit as st
import os
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
image_storage_location="C:\\Users\\Ruman Asif\\Documents\\" \
                       "Personal\\guvi\\projects\\biz card\\pythone proj\\images location"

if uploaded_file is not None:
    # Save the uploaded image to the target folder
    file_path = os.path.join(image_storage_location, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())


# Create two columns
col1, col2 = st.columns(2)

# Place content in the first column
with col1:
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image")



# Place content in the second column
with col2:
    if uploaded_file is not None:
        import easyocr
        import re

        # image = Image.open("C:\\Users\\Ruman Asif\\Documents\\Personal\\guvi\\projects\\biz card\\1.png")

        # Extract text using EasyOCR
        reader = easyocr.Reader(['en'])
        result = reader.readtext(file_path)
        # print(result)
        for each in result:
            print(each[1])
        print(type(result), len(result))
        print()
        print()
        email = ""
        website = ""
        name = result[0][1]
        designation = result[1][1]
        company = result[len(result) - 1][1]
        address = ""
        phone_no = ""
        pattern_for_www = r'^w{3}\s*$'
        pattern_for_phoneno = r'^(?=.*\d)[\d+\-]{9,}$'
        for each in result:
            if '@' in each[1]:
                email = each[1]
            # if (each[1] == 'www'):
            if bool(re.match(pattern_for_www, each[1])):
                website = each[1] + "." + website
            if '.com' in each[1] and "@" not in each[1]:
                website = website + each[1]
            if bool(re.match(pattern_for_phoneno, each[1])):
                phone_no = each[1]
        for i in reversed(range(len(result) - 1)):
            if ".com" in result[i][1] or "@" in result[i][1]:
                break
            address = result[i][1] + " " + address

        st.write("Name:",name)
        st.write("Designation:",designation)
        st.write("Email:",email)
        st.write("Website:", website)
        st.write("Phone no.:", phone_no)
        st.write("address:", address)
        st.write("company:", company)

# Create a button
store_in_sql_clicked = st.button("Store in sql")

# Check if the button is clicked
if store_in_sql_clicked:
    import mysql.connector

    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="serendipity",
        auth_plugin='mysql_native_password'
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS imagetestdb1")
    cursor.execute("USE imagetestdb1")
    # Create the images table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS images1 (
        image_id INT AUTO_INCREMENT PRIMARY KEY,
        image_data LONGBLOB, name varchar(255), designation varchar(255),
        email varchar(255),website varchar(255),phone_no varchar(255),address varchar(255),
        company varchar(255)
    )
    """
    cursor.execute(create_table_query)
    # Read the image file
    with open('1.png', 'rb') as file:
        image_data = file.read()

    # Execute an SQL INSERT statement
    sql = "INSERT INTO images1 (image_data,name,designation,email," \
          "website,phone_no,address,company) VALUES (%s, %s, %s, %s, %s,%s, %s, %s)"
    values=(image_data,name,designation,email,website,phone_no,address,company)
    cursor.execute(sql, values)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    st.write("The above image and extracted data is store in sql database")

display_the_sql_table=st.button("Display the sql table")
if display_the_sql_table:
    from sqlalchemy import create_engine
    import pandas as pd
    # df=pd.DataFrame()
    import pymysql
    engine=create_engine('mysql+pymysql://root:serendipity@localhost/imagetestdb1')
    myQuery='''SELECT * FROM images1'''
    df = pd.read_sql_query(myQuery, engine)
    st.write(df)

#-------------------------edit the table---------------------------
import pymysql
import streamlit as st
# Connect to the MySQL database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='serendipity',
    database='imagetestdb1'
)
cursor = conn.cursor()

# edit_sql_table=st.button("Edit the sql table")
# if edit_sql_table:
image_id = st.text_input("Enter image id number if you want to edit "
                             "from the above table")

if image_id:
    image_id1 = image_id
    image_id1 = int(image_id1)
    query_for_edit = f"select name from images1 where image_id={image_id1}"
    cursor.execute(query_for_edit)
    result = cursor.fetchone()[0]
    name_tt=st.text_input("enter name below",result)
    # st.write(result)

    cursor = conn.cursor()
    query_for_edit = f"select designation from images1 where image_id={image_id1}"
    cursor.execute(query_for_edit)
    result = cursor.fetchone()[0]
    desig_tt = st.text_input("enter designation",result)

    cursor = conn.cursor()
    query_for_edit = f"select email from images1 where image_id={image_id1}"
    cursor.execute(query_for_edit)
    result = cursor.fetchone()[0]
    email_tt = st.text_input("Email:",result)

    cursor = conn.cursor()
    query_for_edit = f"select website from images1 where image_id={image_id1}"
    cursor.execute(query_for_edit)
    result = cursor.fetchone()[0]
    website_tt = st.text_input("Website",result)

    cursor = conn.cursor()
    query_for_edit = f"select phone_no from images1 where image_id={image_id1}"
    cursor.execute(query_for_edit)
    result = cursor.fetchone()[0]
    phone_tt = st.text_input("Phone:",result)

    cursor = conn.cursor()
    query_for_edit = f"select address from images1 where image_id={image_id1}"
    cursor.execute(query_for_edit)
    result = cursor.fetchone()[0]
    address_tt = st.text_input("address",result)
    # st.write(result)
    cursor = conn.cursor()
    query_for_edit = f"select company from images1 where image_id={image_id1}"
    cursor.execute(query_for_edit)
    result = cursor.fetchone()[0]
    company_tt = st.text_input("company",result)
    # st.write(result)
    update_table=st.button("update")

    if update_table:
        cursor = conn.cursor()

        # Execute an SQL UPDATE statement
        sql = "UPDATE images1 SET name = %s, designation = %s, email = %s,website  = %s," \
              "phone_no = %s,address = %s,company = %s WHERE image_id = %s"
        name = name_tt
        designation = desig_tt
        email = email_tt
        website = website_tt
        phone_no = phone_tt
        address = address_tt
        company = company_tt
        image_id = image_id
        values = (name, designation, email, website, phone_no, address, company, image_id)

        cursor.execute(sql, values)
        st.write("Edited")

        # Commit the transaction
        conn.commit()

        # Close the cursor and the connection
        cursor.close()
        conn.close()

image_id_delete=st.text_input("enter the image_id of the row if you want to delete")

delete_row=st.button("delete the above row")
if delete_row:
    delete_query = f"DELETE FROM images1 WHERE image_id={image_id_delete}"
    cursor.execute(delete_query)
    conn.commit()
    cursor.close()
    conn.close()
    st.write("Row deleted, check the table above for verification")


