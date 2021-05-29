import numpy as np
import pandas as pd
import pickle
import cv2


# Load all models
haar = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')
model = pickle.load(open("./model/svm.pickle","rb"))
mean = np.load("./model/pca_50_mean.npz")["arr_1"]
pca = np.load("./model/pca_50_mean.npz",allow_pickle=True)["arr_0"]
pca = pca.tolist()

def pipeline_model(path,filename,color='bgr'):
    img = cv2.imread(path)
    gender = ["male","female"]
    font = cv2.FONT_HERSHEY_SIMPLEX
    if color == "bgr":
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    faces = haar.detectMultiScale(gray,1.5,3)
    for x,y,w,h in faces:
        # print("Face Detected")
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
        roi = gray[y:y+h,x:x+w]
        roi = roi/255.0
        if roi.shape[1] > 100:
            # print("Resized")
            roi_res = cv2.resize(roi,(100,100),cv2.INTER_LINEAR)
        else:
            roi_res = cv2.resize(roi,(100,100),cv2.INTER_CUBIC)
            # print("Resized/")

        res = roi_res.reshape(1,10000) #1,10k
        roi_mean = res - mean
        eigen_image = pca.transform(roi_mean)
        results = model.predict_proba(eigen_image)[0] #probability
        pred = results.argmax() #0 or 1 index for the maximum probability.
        score = results[pred]
        text = "%s : %0.2f"%(gender[pred],score)
        cv2.putText(img,text,(x,y),font,1,(255,255,0),2) #font scale is  1pixel
    cv2.imwrite("static/predict/"+filename,img)

