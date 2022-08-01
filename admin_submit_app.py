from module_config import *
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import import_database
import os
import pandas as pd
import requests
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
from msrest import ServiceClient


ALLOWED_EXTENSIONS = {'xlsx', 'xlsm', 'xlsb', 'xltx', 'xltm', 'xls', 'xlt', 'xml', 'xlam', 'xla', 'xlw', 'xlr', 'ods'}

app = Flask(__name__)
app.config.from_object(BaseConfig()) 

storage_account_name = 'trieudatalake' 
storage_account_key = 'mU+0Nm9y79tgRnsj2QFUyoqtXXNfDPOcidRFaCP+eUYpDH6A14uNgb/ql8sXX7i9wy9y9q/xEHMM+AStlsMMAg=='


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
                # filename = secure_filename(file.filename)

                '''name file, folder'''
                sub_folder =  str(datetime.now().strftime("%d_%m_%Y"))
                date_now   =  str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
                file_name  = f'data_{date_now}.xlsx' 
                file_name_parquet  = f'data_{date_now}' 

                #sub_folder =  str(datetime.now()).replace(":", "").replace(" ", "").replace(".", "").replace("-", "")
                print("Create", sub_folder)

                try: 
                    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], sub_folder))
                    file.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], sub_folder), file_name))
                    # import_database.load_database(storage_account_name, storage_account_key, sub_folder, file_name)
                    path = f'C:\\Users\\Trieu.Nguyen\\Downloads\\WareHouse_Solution\\upload\\{sub_folder}\\{file_name}'
                    path_parquet = f'C:\\Users\\Trieu.Nguyen\\Downloads\\WareHouse_Solution\\upload\\{sub_folder}\\{file_name_parquet}.parquet'
                    print("path: ",path)
                    print("path_parquet: ",path_parquet)

                    df  =  pd.read_excel(path,na_filter=False)
                    df.to_parquet(path_parquet)    
                
                    global service_client
                    service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format("https", storage_account_name), credential=storage_account_key)

                    global file_system_client
                    file_system_client = service_client.get_file_system_client(file_system="datawarehouse")
                    directory_client = file_system_client.get_directory_client(f"Daily\\{sub_folder}")

                    file_client = directory_client.get_file_client(f'{file_name_parquet}.parquet')

                    local_file = open(path_parquet,'rb')
                    file_contents = local_file.read()
                    file_client.upload_data(file_contents, overwrite=True)

                except OSError as error: 
                    print("Error", error)
                flash('Đang tải file lên. ...')
                all_file = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], sub_folder))

                return render_template("upload_form.html", files = all_file)
            else:
                flash('Định dạng không hợp lệ')
    else:
        #do something else
        all_file = []
        pass
    return render_template("upload_form.html", files = all_file) 

if __name__ == '__main__':
    app.run(debug=True, port=5002)
    