from flask import Flask, render_template, request
import pytesseract, cv2, os
from flask_uploads import UploadSet, IMAGES
from PIL import Image

mastered_list = []
learninglist = []

project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            static_url_path= '',
            static_folder='static',
            template_folder='templates')

photos = UploadSet('photos', IMAGES)

app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = 'img'

# Class for image to Text
class GetText(object):
    def __init__(self, file):
        #pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        self.file = pytesseract.image_to_string(Image.open(project_dir + '/img/' + file))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'photo' not in request.files:
            return 'there is no photo in form'
        name = request.form['img-name'] + '.jpg'
        photo = request.files['photo']
        path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        photo.save(path)

        textObject = GetText(name)
        print('TEXT OBJECT' + textObject.file)

        result = textObject.file.split()

        learninglist = result

        return render_template("wordlibrary.html", learning_list=learninglist)

    return render_template('file_upload.html')


@app.route('/wordlibrary', methods=['GET', 'POST'])
def wordlibrary():

    selected_word = request.args.get('add_this_word')
    learninglist = request.args.getlist('learninglist')
    print("Selected word is", selected_word)
    if selected_word != "None":
        if selected_word not in mastered_list:
            mastered_list.append(selected_word)

    return render_template("wordlibrary.html", mastered_list = mastered_list, learning_list = learninglist)

'''
def index():
    return render_template('File upload.html')



@app.route('/', methods=['POST']))


    def upload_file(self):
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)

        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        img = cv2.imread(uploaded_file.filename + '.jpg')

        custom_config = r'--oem 3 --psm 6'
        print(pytesseract.image_to_string(Image.open(uploaded_file.filename)))
        return redirect(url_for('index'))
'''
