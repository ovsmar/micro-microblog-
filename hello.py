from hashlib import sha512
from datetime import datetime
import json
from flask import Flask, render_template , request,redirect

app = Flask(__name__,
            static_url_path='/DATA', 
            static_folder='DATA')

@app.route('/blog/')
def blog():
    return render_template('vue.html')

@app.route('/')
def redirection():
    return redirect('blog')

@app.route('/blog/', methods=['GET'])
def shortenurl():
    now = datetime.now()
    date_time = now.strftime("%Y%m%d%H%M%S")
    if request.method == 'POST':
        form = request.form
        file = './DATA/'+ date_time +'.json'
        with open(file, 'w') as outfile:
            d = {
                "url":"http://127.0.0.1:5000/" +file,
                "contenu":form['contenu'], 
                "date": date_time
            }
            json.dump(d, outfile)

        with open('./DATA/post.json','r') as f:
          results = json.load(f)  
        results.append("http://127.0.0.1:5000/" +file)
        with open('./DATA/post.json','w') as f:
            json.dump(results, f,indent=4)
        return file
    elif request.method == 'GET':
        return 'A GET request was made'
    else:
        return 'Not a valid request method for this route'
        
        
@app.route('/blog/', methods=['POST'])    
def check_secret():
    
        with open('pwd.txt') as test_f:
            datafile = test_f.readline()
            a = request.form["secret"]
            a = a.encode()
            retour = sha512(a).hexdigest()
        if retour == datafile:
            return shortenurl()
        return redirect ("http://127.0.0.1:5000", code=403)




