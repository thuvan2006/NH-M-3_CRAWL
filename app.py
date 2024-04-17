from flask import Flask, request, jsonify
import pymysql
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/crawl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Cấu hình APScheduler
app.config['SCHEDULER_API_ENABLED'] = True
app.config['SCHEDULER_TIMEZONE'] = "UTC"

class Crawl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_list = db.Column(db.JSON, nullable=True)
    year_list = db.Column(db.JSON, nullable=True)
    rating_list = db.Column(db.JSON, nullable=True)
    link_list = db.Column(db.JSON, nullable=True)
    genres_list = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, name_list, year_list, rating_list, link_list, genres_list, deleted_at=None):
        self.name_list = name_list
        self.year_list = year_list
        self.rating_list = rating_list
        self.link_list = link_list
        self.genres_list = genres_list
        self.deleted_at = deleted_at


@app.route('/', methods=['GET'])
def home():
    return "Hello world"

@app.route('/crawl-data/<int:type_id>', methods=['GET'])
def crawl(type_id):
    chrome_driver= webdriver.Chrome()
    chrome_driver.maximize_window()
    url = 'https://www.imdb.com/registration/signin'
    chrome_driver.get(url)
    sleep(2)
    click_singin = chrome_driver.find_element(By.XPATH, '//*[@id="signin-options"]/div/div[1]/a[1]')
    click_singin.click()
    sleep(3)

    with open('login.txt', 'r') as file:
        # Đọc từng dòng trong file
        lines = file.readlines()
        # Gán username và password từ từng dòng
        username = lines[0].strip() # Lấy dòng đầu tiên và loại bỏ khoảng trắng ở hai đầu
        password = lines[1].strip()

        # Tìm phần tử trên trang web bằng id và gán cho biến 'email'
        email_login = chrome_driver.find_element(By.ID, 'ap_email')
        # Gửi dữ liệu (địa chỉ email) vào phần tử email
        email_login.send_keys(username)
        sleep(3)

        password_login = chrome_driver.find_element(By.ID, 'ap_password')
        password_login.send_keys(password)
        sleep(2)

        login = chrome_driver.find_element(By.ID, 'signInSubmit')
        login.click()
        sleep(3)

        menu = chrome_driver.find_element(By.XPATH, '//*[@id="imdbHeader-navDrawerOpen"]')
        menu.click()
        sleep(3)

        # choice = input("Bạn muốn cào dữ liệu từ (nhập số):\n1. TOP 250 MOVIES\n2. POPULAR MOVIES\n")
        if type_id == 1:
            print("1")
            top_chart = chrome_driver.find_element(By.XPATH, '//*[@id="imdbHeader"]/div[2]/aside[1]/div/div[2]/div/div[1]/span/div/div/ul/a[2]')
            top_chart.click()
            sleep(3)
            soup = BeautifulSoup(chrome_driver.page_source, 'html.parser')
            nameList=[]
            yearList=[]
            ratingList=[]
            linkList=[]
            Lists= soup.findAll('li', {'class':'ipc-metadata-list-summary-item'})
            for List in Lists:
                name= List.find('div', {'class':'cli-children'}).a.text
                nametemp=  name.split('. ')[1]
                nameList.append(nametemp) 
                year = List.find('div', {'class':'cli-title-metadata'}).text[0:4]
                yearList.append(year)
                rating =  List.find('div', {'data-testid':'ratingGroup--container'}).text[0:3]
                ratingList.append(rating)
                a_tag = List.find('div', {'class': 'cli-children'}).a
                if a_tag:
                    link = f'https://www.imdb.com{a_tag["href"]}'
                    linkList.append(link)
            # In ra danh sách các liên kết đã được trích xuất
            for link in linkList:
                soup = BeautifulSoup(chrome_driver.page_source, 'html.parser')
                url = 'link'
                genres= soup.findAll('span', {'class':'ipc-chip__text'})
                # Tạo một danh sách để lưu trữ các thể loại của phim
                genresList = []
                
                # Duyệt qua từng thẻ span và thêm thể loại vào danh sách
                for genre in genres:
                    genresList.append(genre.text)
                genresList.append(", ".join(genresList))
        elif type_id == 2:
            print("2")
            popular_movie = chrome_driver.find_element(By.XPATH, '//*[@id="imdbHeader"]/div[2]/aside[1]/div/div[2]/div/div[1]/span/div/div/ul/a[3]')
            popular_movie.click()
            sleep(3)
            soup = BeautifulSoup(chrome_driver.page_source, 'html.parser')
            nameList=[]
            yearList=[]
            ratingList=[]
            linkList=[]
            Lists= soup.findAll('li', {'class':'ipc-metadata-list-summary-item'})
            for List in Lists:
                name= List.find('div', {'class':'cli-children'}).a.text
                nameList.append(name) 
                year = List.find('div', {'class':'cli-title-metadata'}).text[0:4]
                yearList.append(year)
                rating =  List.find('div', {'data-testid':'ratingGroup--container'}).text[0:3]
                ratingList.append(rating)
                a_tag = List.find('div', {'class': 'cli-children'}).a
                if a_tag:
                    link = f'https://www.imdb.com{a_tag["href"]}'
                    linkList.append(link)
            # In ra danh sách các liên kết đã được trích xuất
            for link in linkList:
                soup = BeautifulSoup(chrome_driver.page_source, 'html.parser')
                url = 'link'
                genres= soup.findAll('span', {'class':'ipc-chip__text'})
                # Tạo một danh sách để lưu trữ các thể loại của phim
                genresList = []
                
                # Duyệt qua từng thẻ span và thêm thể loại vào danh sách
                for genre in genres:
                    genresList.append(genre.text)
                genresList.append(", ".join(genresList))
        else:
            print('Lựa chọn không hợp lệ')
            return "fails"

        # Xóa tất cả các record trong bảng Crawl
        # db.session.query(Crawl).delete()
        # db.session.commit()

        new_crawl = Crawl(name_list=nameList, year_list=yearList, rating_list=ratingList, link_list=linkList, genres_list=genresList)
        db.session.add(new_crawl)
        db.session.commit()

        print('Data saved successfully!')

    return "Data saved successfully!", 200

@app.route('/get-crawl-data', methods=['GET'])
def get_crawl_data():
    crawl_record = Crawl.query.first()
    if crawl_record:
        return jsonify({
            "name_list": crawl_record.name_list,
            "year_list": crawl_record.year_list,
            "rating_list": crawl_record.rating_list,
            "link_list": crawl_record.link_list,
            "genres_list": crawl_record.genres_list,
            "status": "success"
        })
    else:
        return jsonify({
            "status": "error",
            "message": "No data available"
        }), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
