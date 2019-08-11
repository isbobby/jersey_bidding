from jersey_bidder import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

#run with: export FLASK_APP=flaskblog.py 
#          FLASK_ENV=development flask run 
#under directory