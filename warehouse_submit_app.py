from module_config import *

app = Flask(__name__)
app.config.from_object(BaseConfig()) 

ALLOWED_EXTENSIONS = {'xlsx', 'xlsm', 'xlsb', 'xltx', 'xltm', 'xls', 'xlt', 'xml', 'xlam', 'xla', 'xlw', 'xlr', 'ods'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 
           
@app.route('/', methods=['GET', 'POST'])
def home():
    all_file = []
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('Chưa chọn file')
        else:
            if file and allowed_file(file.filename):
                
                #Add data to database
                #end
                
                pass
            else:
                flash('Định dạng không hợp lệ')
    else:
        #do something else
        all_file = []
        pass
    return render_template("upload_form_2.html", files = all_file)

if __name__ == '__main__':
    app.run(debug=True, port=5004)
    