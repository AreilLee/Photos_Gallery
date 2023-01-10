# Photos_Gallery
A simple photo gallery, easy to use, manage, and present. The functions including add, edit, and delete. Can check all the data with SQL.
The most challenged part was intall a captcha in login part. I'm really glad I made it.
## Description
### install captcha in the Django envirnment
```
pip install django-simple-captcha
``` 
### Put 'captcha' and CAPTCHA_NOISE_FUNCTIONS in INSTALLED_APPS(setting.py)
### Migrate captcha in cmd
```
python manage.py migrate
``` 
### Create a form.py to set a class
![image](https://user-images.githubusercontent.com/121281901/211549038-05366e4f-164e-4dea-84f9-f7b56cec6aea.png)
### link captcha into login.html
![image](https://user-images.githubusercontent.com/121281901/211550552-80350ac7-57c2-48d6-b931-0efa8eb88253.png)

## Outcome
![image](https://user-images.githubusercontent.com/121281901/211550631-4c5f05ad-b1ae-41a0-b2ef-c9ce60615e50.png)

## Acknowledgments
* All the pictures were taken by the program author(me :)).
