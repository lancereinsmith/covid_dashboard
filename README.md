# covid_dashboard

https://gilberttanner.com/blog/deploying-your-streamlit-dashboard-with-heroku

git init


heroku login

heroku create

heroku config:set STREAMLIT_EMAIL=email@address.com

git add .
git commit -m "Initial commit"
git push heroku master

heroku ps:scale web=1