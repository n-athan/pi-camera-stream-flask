#Modified by smartbuilds.io and n-athan
#Date: 03.08.2022
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
import http.server # Our http server handler for http requests
import socketserver # Establish the TCP Socket connections
import urllib
from camera import VideoCamera
import os

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

PORT = 5000 
HOST = "0.0.0.0"
class MyHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    def gen(camera):
        #get camera frame
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
    def do_GET(self):
        # parsed_path = urllib.parse.urlparse(self.path)
        if (self.path == '/video_stream'): 
            self.send_response(200)
            self.send_header("Content-type", "multipart/x-mixed-replace; boundary=frame")
            self.end_headers()

            self.wfile.write(MyHttpRequestHandler.gen(pi_camera))
            # return Response(gen(pi_camera), mimetype='multipart/x-mixed-replace; boundary=frame')
        elif (self.path == '/picture'):
            pi_camera.take_picture()
            return "None"
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open('/template/index.html', 'utf-8') as file: 
                self.wfile.write(file.read()) # Read the file and send the contents 
 
Handler = MyHttpRequestHandler
 
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Http Server Serving at", HOST, ":", PORT)
    httpd.serve_forever()



# # App Globals (do not edit)
# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html') #you can customze index.html here

# def gen(camera):
#     #get camera frame
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(pi_camera),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# # Take a photo when pressing camera button
# @app.route('/picture')
# def take_picture():
#     pi_camera.take_picture()
#     return "None"

# if __name__ == '__main__':

#     app.run(host='0.0.0.0', debug=False)
