Install
npm install -g newman
npm install newman-reporter-html


#To run newman tests

newman run User_Management_API.postman_collection.json -e user_manage.postman_environment.json -r html --reporter-html-export report.html

#For specific folder

newman run User_Management_API.postman_collection.json -e user_manage.postman_environment.json --folder "User CRUD flow" --reporters cli