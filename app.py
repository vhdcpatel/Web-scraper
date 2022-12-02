from flask import Flask, render_template,request,redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import os
from modules import main
from modules2 import main2, delete_tables
from modules3 import main3


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        query = request.form['query']
        
        response = main(query)
        if response == 1:
            print("Data loaded to sqlite")
            return render_template('sucess.html')
        else:
            print("Data not loaded")
            return render_template('failure.html')
        # return redirect("/")

    return render_template('index.html')

@app.route('/data')
def data_list():
    name_list,size_list = main2()
    if name_list == None:
        return render_template("no_table.html")

    else:
        name_link_list = zip(name_list,size_list) 
        return render_template("downloads.html",name_link_list = name_link_list) 


@app.route('/download/<file_name>')
def download(file_name):
    df = main3(file_name)
    path = os.path.join("./","Data")

    if(f"./{file_name}.csv") in os.listdir("./Data"):
        temp  =10
        return send_file(f"./Data/{file_name}.csv")
    else:
        df.to_csv(f"{path}/{file_name}.csv")
        return send_file(f"./Data/{file_name}.csv")


@app.route("/reset")
def reset_db():
    db_name = 'WS_data'
    delete_tables(db_name)
    return redirect('/')

@app.route("/info")
def infomation():
    return render_template('info.html')

    
if __name__ == '__main__':
  app.run(debug=True,port=8000)