from django.shortcuts import render 
import keras
from PIL import Image
import numpy as np 
import os
from django.core.files.storage import FileSystemStorage

media = 'media'
model = keras.models.load_model('potato.h5')
classes_name = {0:"Early bright",
                1:"Late Bright",
                2:"Healthy" 
}
diseases_info = {
    0:"In most production areas, early blight occurs annually to some degree. The severity of early blight is dependent upon the frequency of foliar wetness from rain, dew, or irrigation; the nutritional status of the foliage; and cultivar susceptibility.The first symptoms of early blight appear as small, circular or irregular, dark-brown to black spots on the older (lower) leaves. These spots enlarge up to 3/8 inch in diameter and gradually may become angular-shaped.Initial lesions on young, fully expanded leaves may be confused with brown spot lesions. These first lesions appear about two to three days after infection, with further sporulation on the surface of these lesions occurring three to five days later.",
    1:"The primary host is potato, but P. infestans also can infect other solanaceous plants, including tomatoes, petunias and hairy nightshade, that can act as source of inoculum to potato.The first symptoms of late blight in the field are small, light to dark green, circular to irregular-shaped water-soaked spots. These lesions usually appear first on the lower leaves. Lesions often begin to develop near the leaf tips or edges, where dew is retained the longest.During cool, moist weather, these lesions expand rapidly into large, dark brown or black lesions, often appearing greasy. Leaf lesions also frequently are surrounded by a yellow chlorotic halo",
    2:"Many potatoes need consistent moisture levels to develop, so water regularly on a daily basis when tubers establish. When you the water the potato plants it should reach to the ground level of about 8-10 inches. During hot or warm seasons water the potato plants in huge amounts twice a day as the soil gets dry quickly."
}
def makepredicitions(path):
    img = Image.open(path)
    img_d = img.resize((256,256))
    if len(np.array(img_d).shape)<4:
        rgb_img = Image.new("RGB",img_d.size)
        rgb_img.paste(img_d)
    else:
        rgb_img = img_d
    
    rgb_img = np.array(rgb_img,dtype=np.float64)
    rgb_img = rgb_img.reshape(1,256,256,3)

    prediction = model.predict(rgb_img)
    prediction = prediction[0]
    max_index = np.argmax(prediction)
    class_name = classes_name.get(max_index)
    disease = diseases_info.get(max_index)
    confidence = round(100 * (np.max(prediction)),2)
    return class_name , confidence,disease

def index(request):
    if request.method == "POST" and request.FILES['upload']:
        if 'upload' not in request.FILES:
            err = "NO images selected"
            return render(request,'potato.html',{'err':err})
        f = request.FILES['upload']
        if f == '':
            err = "No files selected"
            return render(request,'potato.html',{'err':err})
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name,upload)
        file_url = fss.url(file)
        prediction,confidence,disease = makepredicitions(os.path.join(media,file))
        return render(request,'potato.html',{'pred':prediction,'conf':confidence,'disease':disease,'file_url':file_url})
    
    else:
        return render(request,'potato.html')
    
