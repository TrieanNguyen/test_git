from module_config import *

app = Flask(__name__)
app.config.from_object(BaseConfig()) 

'''info connect to azure sql database'''
server        = Info.server
database      = Info.database
username      = Info.username
password      = Info.password  
driver        = Info.driver

@app.route('/', methods=['GET', 'POST'])
def home():
    DBO   = 'dbo'
    TABLE_NAME = 'TBL_DATA_REGISTER'
    '''command sql '''
    #sql           = f'delete from {DBO}.{TABLE_NAME}'
    #sql =  f'UPDATE {DBO}.{TABLE_NAME} set age = 9 WHERE age =8'

    message = ""
    title = ""
    messDisplay = ""

    if request.method == "POST":
        print(request.form)
        name = request.form['name']
        phone = request.form['phone']
        plate = request.form['plate']
        book = request.form['book']

        
        if(not name or not plate):
            title= 'Cảnh báo!'
            message = 'Bạn phải nhập tên và biển số xe.'
            messDisplay = "inline"
            return render_template('register_info.html', title=title, message= message)

        elif(not book):

            title= 'Cảnh báo!'
            message = 'Bạn phải nhập số tấn book.'
            messDisplay = "inline"
            return render_template('register_info.html', title=title, message= message)

        else:
            try:
                STRING = "'"
                name = str(request.form['name'])
                phone = str(request.form['phone'])
                plate = str(request.form['plate'])
                book = str(request.form['book'])
                time = '1'
                
                sql = f'insert into  {DBO}.{TABLE_NAME} (Name,License_Plate,Weight,Telephone,Time) VALUES  ({STRING}{name}{STRING},{STRING}{phone}{STRING},{STRING}{plate}{STRING},{STRING}{book}{STRING},{STRING}{time}{STRING})'
                print('sql: ', sql)
                with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+'; UID='+username+';PWD='+ password) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(sql)

                title= 'Thông báo!'
                message  = 'Bạn đã đăng kí thành công.'
                messDisplay = "inline"

                return render_template('register_info.html', title=title, message= message)

            except Exception as e:
                title= 'Chú ý!'
                message = 'Có lỗi khi đăng kí, vui lòng thử lại.'
                messDisplay = "inline"

    elif request.method == "GET":
        messDisplay = "none"

    return render_template('register_info.html', title=title, message= message)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    