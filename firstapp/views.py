from django.shortcuts import render 
import keras
from PIL import Image
import numpy as np 
import os
from django.core.files.storage import FileSystemStorage

media = 'media'
model = keras.models.load_model('rice.h5')
classes_name = {0:'Bacterial leaf blight',1:'Bacterial leaf streak',2:'Bakanae',3:'Brown Spot',
 4:'Grassy stunt virus',
 5:'Healthy rice plant',
 6:'Narrow brown spot',
 7:'Ragged stunt virus',
 8:'Rice blast',
 9:'Rice false smut',
 10:'Sheath blight',
 11:'Sheath rot',
 12:'Stem rot',
 13:'Tungro Virus' 
}
diesases_info={
    0:" The disease is most likely to develop in areas that have weeds and stubbles of infected plants. It can occur in both tropical and temperate environments, particularly in irrigated and rainfed lowland areas. In general, the disease favors temperatures at 25−34°C, with relative humidity above 70%.It is commonly observed when strong winds and continuous heavy rains occur, allowing the disease-causing bacteria to easily spread through ooze droplets on lesions of infected plants. ",
    1:" Bacterial leaf streak occurs in areas with high temperature and high humidity. Infected plants show browning and drying of leaves. Under severe conditions, this could lead to reduced grain weight due to loss of photosynthetic area. Particularly, the disease is common in tropical and subtropical regions of Asia, Africa (including Madagascar), South America, and Australia. It can affect the plant during early stages, from maximum tillering to panicle initiation. Mature rice plants can easily recover from leaf streak and have minimal grain yield losses. ",
    2:" Bakanae is a seedborne fungal disease. The fungus infects plants through the roots or crowns. It then grows systemically within the plant. Infected plants are abnormally tall with pale, thin leaves, produce fewer tillers, and produce only partially filled or empty grains. The disease occurs most frequently when infested seeds (i.e., seeds covered in fungal spores) are used, but also can occur when the pathogen is present on plant material or in the soil. It spreads through wind or water that carries the fungal spores from one plant to another.  ",
    3:" Brown spot has been historically largely ignored as one of the most common and most damaging rice diseases. Its most observable damage is the numerous big spots on the leaves which can kill the whole leaf. When infection occurs in the seed, unfilled grains or spotted or discolored seeds are formed. Brown spot can occur at all crop stages, but the infection is most critical during maximum tillering up to the ripening stages of the crop. ",
    4:" Rice grassy stunt virus affects rice crops in areas where continuous and year-round rice growing is practiced. The virus is transmitted between plants by insect vectors. Nymph and adult stage plant hoppers are common vectors for rice grassy stunt virus. The plant hoppers need to feed on an infected plant for at least 30 minutes to pick-up the virus. Plants can be infected at all growth stages. They are most vulnerable to infection at the tillering stage. Rice grassy stunt virus symptoms develop 10−12 days after infection. Infected stubble and volunteer rice are sources of rice grassy stunt virus. It cannot be transmitted via brown planthopper eggs. ",
    5:"Prepare the soil so that it has a good supply of nutrients and keep the soil well aerated. SRI soil management practices -- no flooding, and the use of compost -- help microorganisms in the soil to produce more nitrogen for the rice plants, and it is well known that plant roots require oxygen.  ",
    6:" The disease usually occurs in potassium deficient soils, and in areas with temperature ranging from 25−28°C. It appears during the late growth stages of the rice crop, starting at heading stage. Plants are most susceptible during panicle initiation onwards, and damage becomes more severe as plants approach maturity.  ",
    7:" Rice ragged stunt virus reduces yield by causing partially exerted panicles, unfilled grains and plant density loss. It is vector-transmitted from one plant to another by brown plant hoppers. Leaves of infected plants have a ragged appearance. Rice ragged stunt virus infection is particularly high in tropical conditions where rice is planted all-year-around and provides a continuous host for the brown plant hopper vector.  ",
    8:" Blast is caused by the fungus Magnaporthe oryzae. It can affect all above ground parts of a rice plant: leaf, collar, node, neck, parts of panicle, and sometimes leaf sheath. It occurs in areas with low soil moisture, frequent and prolonged periods of rain shower, and cool temperature in the daytime. In upland rice, large day-night temperature differences that cause dew formation on leaves and overall cooler temperatures favor the development of the disease. ",
    9:" False smut causes chalkiness of grains which leads to reduction in grain weight. It also reduces seed germination. The disease can occur in areas with high relative humidity (>90%) and temperature ranging from 25−35 ºC.  Rain, high humidity, and soils with high nitrogen content also favors disease development. Wind can spread the fungal spores from plant to plant. False smut is visible only after panicle exsertion. It can infect the plant during flowering stage. ",
    10:" Sheath blight is a fungal disease caused by Rhizoctonia solani. Infected leaves senesce or dry out and die more rapidly, young tillers can also be destroyed. As a result, the leaf area of the canopy can significantly be reduced by the disease. This reduction in leaf area, along with the diseased-induced senescence of leaves and young infected tillers are the primary causes of yield reduction. ",
    11:" The disease reduces grain yield by retarding or aborting panicle emergence, and producing unfilled seeds and sterile panicles. Sheath rot also reduces grain quality by causing panicles to rot and grains to become discolored. ",
    12:" Stem rot leads to formation of lesions and production of chalky grains and unfilled panicles. The infection bodies or sclerotia are found in the upper soil layer. They survive in air-dry soil, buried moist rice soil, and in tap water. They can also survive on straw, which is buried in the soil. The sclerotia float on irrigation water and infect newly planted rice during land preparation.  ",
    13:" Rice tungro disease is caused by the combination of two viruses, which are transmitted by leafhoppers. It causes leaf discoloration, stunted growth, reduced tiller numbers and sterile or partly filled grains. Tungro infects cultivated rice, some wild rice relatives and other grassy weeds commonly found in rice paddies. "
}

def home(request):
    return render(request,'home.html')

def contact(request):
    return render(request,'contact.html')

def makepredicitions(path):
    img = Image.open(path)
    img_d = img.resize((224,224))
    if len(np.array(img_d).shape)<4:
        rgb_img = Image.new("RGB",img_d.size)
        rgb_img.paste(img_d)
    else:
        rgb_img = img_d
    
    rgb_img = np.array(rgb_img,dtype=np.float64)
    rgb_img = rgb_img.reshape(1,224,224,3)

    prediction = model.predict(rgb_img)
    prediction = prediction[0]
    max_index = np.argmax(prediction)
    class_name = classes_name.get(max_index)
    disease = diesases_info.get(max_index)
    confidence = round(100 * (np.max(prediction)),2)
    return class_name , confidence,disease

def index(request):
    if request.method == "POST" and request.FILES['upload']:
        if 'upload' not in request.FILES:
            err = "NO images selected"
            return render(request,'rice.html',{'err':err})
        f = request.FILES['upload']
        if f == '':
            err = "No files selected"
            return render(request,'rice.html',{'err':err})
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name,upload)
        file_url = fss.url(file)
        prediction,confidence,disease = makepredicitions(os.path.join(media,file))
        return render(request,'rice.html',{'pred':prediction,'conf':confidence,'disease':disease,'file_url':file_url})
    
    else:
        return render(request,'rice.html')
    
