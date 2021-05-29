from flask import Flask
from app.views import base,index,faceapp,gender

app = Flask(__name__)



app.add_url_rule("/base","base",base)
app.add_url_rule("/","index",index)
app.add_url_rule("/faceapp","faceapp",faceapp)
app.add_url_rule("/faceapp/gender","gender",gender, methods=["GET","POST"])




if __name__ == "__main__":
    app.run(debug=True)



