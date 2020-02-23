# importing dependencies module
import os
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import urllib.request
import csv
import glob
import cv2


# #PageNoDirectoryCreation
# for i in range(1,11):
#     dirname = f"PageNo{i}"
#     parent_dir = r"C:\Users\Lenovo\Desktop\Task\Pure"
#     path = os.path.join(parent_dir, dirname)
#     os.mkdir(path)
#     dirname2 = "CSV Data"
#     dirname3 = "Images"
#     parent_dir1 = f"C:\\Users\\Lenovo\\Desktop\\Task\\PageNo{i}"
#     path1 = os.path.join(parent_dir1, dirname2)
#     path2 = os.path.join(parent_dir1, dirname3)
#     os.mkdir(path1)
#     os.mkdir(path2)
#     dirname4 = "AllImages"
#     dirname5 = "CroppedImages"
#     parent_dir2 = f"C:\\Users\\Lenovo\\Desktop\\Task\\PageNo{i}\\Images"
#     path3 = os.path.join(parent_dir2, dirname4)
#     path4 = os.path.join(parent_dir2, dirname5)
#     os.mkdir(path3)
#     os.mkdir(path4)
#----------------------------------------------------------------------------


dirname = f"PageNo1"
parent_dir = r"C:\Users\Lenovo\Desktop\Task"
path = os.path.join(parent_dir, dirname)
os.mkdir(path)
dirname2 = "CSVData"
dirname3 = "Images"
parent_dir1 = f"C:\\Users\\Lenovo\\Desktop\\Task\\PageNo1"
path1 = os.path.join(parent_dir1, dirname2)
path2 = os.path.join(parent_dir1, dirname3)
os.mkdir(path1)
os.mkdir(path2)
dirname4 = "AllImages"
dirname5 = "CroppedImages"
parent_dir2 = f"C:\\Users\\Lenovo\\Desktop\\Task\\PageNo1\\Images"
path3 = os.path.join(parent_dir2, dirname4)
path4 = os.path.join(parent_dir2, dirname5)
os.mkdir(path3)
os.mkdir(path4)
#----------------------------------------------------------------------------


#Part -1 Scrapping Data-working on online data

#Intializations
count = 1
session = HTMLSession()
response = session.get("http://www.cutestpaw.com/tag/cats/page/1/").html
source = response.html
soup = BeautifulSoup(source, "lxml")

#Lists
titlesList = []
hyperList = []
imgurls = []

#Scraping Part
whole_box = soup.find(id="photos")
print(type(whole_box))
all_boxes = whole_box.find_all("a")

#Writing Main Rows of CSV here
# with open(r'C:\Users\Lenovo\Desktop\Task\PageNo1\CSV Data\AllData.csv', "a") as s:
#     file=csv.writer(s)
#     file.writerow(("Title", 'Hyperlink'))
    

for one_box in all_boxes:
    #title stuff
    title = one_box.find("img")
    title = title.attrs['title']
    titlesList.append(title + "\n")
    
    #Hyperlinks
    hyper = one_box.attrs['href']
    hyperList.append(hyper + '\n')
    
    #imageUrl
    imgurl = one_box.find("img")
    imgurl = imgurl.attrs['src']
    imgurls.append(imgurl)
    try:
        urllib.request.urlretrieve(imgurl, f"C:\\Users\\Lenovo\\Desktop\\Task\\PageNo1\\Images\\AllImages\\{title}.jpg")
        print("Downloaded Image No:", count)

    except:
        imgurl = "http://www.cutestpaw.com/wp-content/uploads/2016/02/s-Kitty-yoga.%281%29.jpg"
        urllib.request.urlretrieve(
            imgurl, f"C:\\Users\\Lenovo\\Desktop\\Task\\PageNo1\\Images\\AllImages\\{title}.jpg")
        print("Downloaded Image No:", count)
    count += 1


    #writer
    with open(r'C:\Users\Lenovo\Desktop\Task\PageNo1\CSVData\AllData.csv', "a") as s:
        file = csv.writer(s)
        file.writerow((title, hyper))


#Part 2 working on offline data---Face Detection part

#accessing images for detection
imgpatternlist = glob.glob("C:\\Users\\Lenovo\\Desktop\\Task\\PageNo1\\Images\\AllImages\\*.jpg")
# print(imgpatternlist)

for image in imgpatternlist:
    print(image)
    face_cascade = cv2.CascadeClassifier(r'C:\Users\Lenovo\Desktop\Task/haarcascade_frontalcatface.xml')
    img = cv2.imread(image, 1)
    grey_img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
    faces = face_cascade.detectMultiScale(grey_img, scaleFactor=1.02, minNeighbors=3)
    # print(type(faces))
    for x, y, w, h in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + w), (0, 255, 0), 3)

    cv2.imshow("Demo", img)
    cv2.waitKey(1)
    if type(faces) == tuple:
        pass
    else:
        # cropped = img[y:y + h, x:x + w]
        # imgv2 = cv2.imshow("Cropped V", cropped)
        imgv2=img
        tempimgpt = image
        tempimgpt = tempimgpt[55:]
        for i in range(1,51):
            cv2.imwrite(f'C:\\Users\\Lenovo\\Desktop\\Task\\PageNo1\\Images\\CroppedImages\\{tempimgpt}' + 'croppedface{i}.jpg', imgv2)
        ctitles = []
        chyper = []
        ctitle=tempimgpt
        ctitles.append(ctitle)
        chyper1='hello'
        chyper.append(chyper1)
        with open(r'C:\Users\Lenovo\Desktop\Task\PageNo1\CSVData\CroppedData.csv', "a") as s:
            file = csv.writer(s)
            file.writerow((ctitle, hyper))
cv2.destroyAllWindows()
