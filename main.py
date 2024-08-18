# from replit import web
from flask import Flask, render_template, make_response
import random
import os
import dropbox

app = Flask(__name__)


@app.route("/",methods=["GET"])
def home():
  # dropbox_token = os.getenv("dropbox_token_access")

  # Create a Dropbox object using an access token
  # dbx = dropbox.Dropbox(dropbox_token)
  dbx = dropbox.Dropbox(
            app_key = os.getenv("APP_KEY"),
            app_secret = os.getenv("APP_SECRET"),
            oauth2_refresh_token = os.getenv("REFRESH_TOKEN")
        )

  # Specify the path to the folder on Dropbox
  folder_path = "/Photos"
  images=[]
  # List all the files in the folder
  try:
      result = dbx.files_list_folder(folder_path,limit=2000)
      for entry in result.entries:
        images.append(entry.name)
        
  except dropbox.exceptions.ApiError as err:
      print("An error occurred:", err)

  # print(len(images))   #To count the number of images in my database.
  random_image = random.choice(images)
  
  
  # Specify the path to the file on Dropbox
  file_path = f"/Photos/{random_image}"
  
  # Get a temporary URL for the file
  url = dbx.files_get_temporary_link(file_path).link
  #print("The URL for the file is: ",url)
  
  # return url
  return render_template("index.html",random_image=url)


if __name__ == '__main__':
#   web.run(app)
  app.run(debug=True)  # Use this to run the app locally