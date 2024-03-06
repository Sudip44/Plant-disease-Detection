from django.shortcuts import render 
import keras
from PIL import Image
import numpy as np 
import os
from django.core.files.storage import FileSystemStorage

media = 'media'
model = keras.models.load_model('tomato.h5')
classes_name = {0:"Early blight",
                1:"Late Blight",
                2:"Two spotted spider mite" ,
                3:"Healthy"
}
diseases_info={ 0:"Early blight is one of the most common tomato diseases, occurring nearly every season wherever tomatoes are grown.It affects leaves, fruits and stems and can be severely yield limiting when susceptible cultivars are used and weather is favorable.Severe defoliation can occur and result in sunscald on the fruit.Early blight is common in both field and high tunnel tomato production in Minnesota.",
               1:"Late blight is caused by the oomycete Phytophthora infestans. Oomycetes are fungus-like organisms also called water molds, but they are not true fungi.There are many different strains of P. infestans. These are called clonal lineages and designated by a number code (i.e. US-23). Many clonal lineages affect both tomato and potato, but some lineages are specific to one host or the other.Late blight is a potentially devastating disease of tomato and potato, infecting leaves, stems and fruits of tomato plants.The disease spreads quickly in fields and can result in total crop failure if untreated.Late blight of potato was responsible for the Irish potato famine of the late 1840s.",
               2:" The two-spotted spider mite is the most common mite species that attacks vegetable and fruit crops in New England. Spider mites can occur in tomato, eggplant, potato, vine crops such as melons, cucumbers, and other crops. Two-spotted spider mites are one of the most important pests of eggplant. They have up to 20 generations per year and are favored by excess nitrogen and dry and dusty conditions. Outbreaks are often caused by the use of broad-spectrum insecticides which interfere with the numerous natural enemies that help to manage mite populations. As with most pests, catching the problem early will mean easier control. ",
               3:" Fertilize one week before as well as on the day of planting. They especially love phosphorous, which promotes the formation of blossoms and the fruits or vegetables that grow from them. Avoid high nitrogen when your tomato plants have blossoms as it promotes vine growth rather than fruit growth.Don't Crowd Tomato Seedlings.Provide Lots of Light.Preheat the Garden Soil.Bury the Stems.Mulch Tomatoes After the Soil Has Warmed.Remove the Bottom Leaves.Pinch and Prune for More Tomatoes.Water Regularly. "

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
    return class_name , confidence, disease

def index(request):
    if request.method == "POST" and request.FILES['upload']:
        if 'upload' not in request.FILES:
            err = "NO images selected"
            return render(request,'tomato.html',{'err':err})
        f = request.FILES['upload']
        if f == '':
            err = "No files selected"
            return render(request,'tomato.html',{'err':err})
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name,upload)
        file_url = fss.url(file)
        prediction,confidence, diesease = makepredicitions(os.path.join(media,file))
        return render(request,'tomato.html',{'pred':prediction,'conf':confidence, 'disease':diesease,'file_url':file_url})
    
    else:
        return render(request,'tomato.html')
    

