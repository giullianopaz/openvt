import os
from search import image_search
from flask import Flask, request, render_template, send_from_directory

__author__ = 'giullianopaz'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
print(" Root path: ", APP_ROOT)


@app.route("/")
def index():
    return render_template("query_result.html")


@app.route("/search", methods=["POST"])
def search():
    target = os.path.join(APP_ROOT, 'uploaded')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for search in request.files.getlist("file"):
        print(search)
        print("{} is the file name".format(search.filename))
        filename = search.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        search.save(destination)

    # image_list = os.listdir('./images')
    # print(image_list)
    
    top_images = image_search(query_path="uploaded/"+filename, hist_comp_method=4, top_n_results=18)
    # print("\n\n top_images: ", top_images)
    return render_template("query_result.html", image_list=top_images, query=filename)


@app.route('/search/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

# @app.route('/gallery')
# def get_gallery():
#     image_list = os.listdir('./images')
#     print(image_list)
#     return render_template("gallery.html", image_list=image_list)


if __name__ == "__main__":
    app.run(port=5000, debug=False)
