from detecto import core, utils, visualize
from detecto.visualize import show_labeled_image, plot_prediction_grid
from lorem_text import lorem
import torch
import numpy as np
import json, itertools, argparse, os
import shutil


from detecto.core import Model


def merge_bounding_box(itterations, filtered_boxes, filtered_labels):
    
    filtered_boxes = filtered_boxes.tolist()
    j = 0

    while j < itterations:
        
        
        for x,y in itertools.combinations(range(len(filtered_labels)), 2):
            try:
                # print(x,y)      

                if filtered_labels[x] == filtered_labels[y]:
                    

                    x0min = filtered_boxes[x][0]
                    y0min = filtered_boxes[x][1]
                    x0max = filtered_boxes[x][2]
                    y0max = filtered_boxes[x][3]
                    
                    x1min = filtered_boxes[y][0]
                    y1min = filtered_boxes[y][1]
                    x1max = filtered_boxes[y][2]
                    y1max = filtered_boxes[y][3]

                    if ((x0min <= x1min <= x0max or x0min <= x1max <= x0max) and (y0min <= y1min <= y0max or y0min <= y1max <= y0max)) or (x1min <= x0min and x1max >= x0max and y1min <= y0min and y1max >= y0max):
                        print(True)
                        x2min = min(x0min,x1min)
                        x2max = max(x0max, x1max)

                        y2min = min(y0min, y1min)
                        y2max = max(y0max, y1max)

                        filtered_labels.append(filtered_labels[x])
                        filtered_boxes.append([x2min,y2min,x2max,y2max])
                        
                        filtered_boxes.pop(y)
                        filtered_boxes.pop(x)

                        filtered_labels.pop(y)
                        filtered_labels.pop(x)
                        break
            except Exception as e:
                break
                print(e)
        j += 1

    filtered_boxes = torch.FloatTensor(filtered_boxes)

    return filtered_boxes, filtered_labels

def predict(model, input):
    thresh = 0.9
    image = utils.read_image(f"{input}") 
    predictions = model.predict(image)
    labels, boxes, scores = predictions


    filtered_indices=np.where(scores>thresh)
    filtered_scores=scores[filtered_indices]
    filtered_boxes=boxes[filtered_indices]
    num_list = filtered_indices[0].tolist()
    filtered_labels = [labels[i] for i in num_list]

    filtered_boxes, filtered_labels = merge_bounding_box(5, filtered_boxes, filtered_labels)

    # show_labeled_image(image, filtered_boxes, filtered_labels)
    return filtered_boxes, filtered_labels

def prediction_to_json(filtered_boxes, filtered_labels, image):
    jsonList = []

    for i in range(len(filtered_boxes)):
        tempDict = {
            "image": str(image),
            "element": str(filtered_labels[i]),
            "Xmin": float(filtered_boxes[i][0]),
            "Ymin": float(filtered_boxes[i][1]),
            "Xmax": float(filtered_boxes[i][2]),
            "Ymax": float(filtered_boxes[i][3]),
        }
        jsonList.append(tempDict)

    return jsonList

    jsonString = json.dumps(jsonList)

    # with open(f'json/{args.input[:-4]}.json', 'w') as outfile:
    #   outfile.write(jsonString)

def json_to_html(elementDict, name="0"):

    try: 
        shutil.copytree("placeholder", f"result-{name}") 

    except Exception as e: 
        print(e)  

    htmlString = ""

    Y_priority = sorted(elementDict, key=lambda d: d['Ymin'])

    for i in Y_priority: 
        x = round((i['Xmin'] / 32)) + 1
        y = round((i['Ymin'] / 32)) + 1

        w = round(((i["Xmax"] - i["Xmin"]) / 32))
        h = round(((i["Ymax"] - i["Ymin"]) / 32))


        # element
        if i["element"] == "checkbox":
            element = f'<div class="c-checkbox" style="grid-column:{x} / span {w};grid-row:{y} / span {h};"><label class="switch"> <input type="checkbox"><span class="slider round"></span></label></div>'
        
        elif i["element"] == "heading":
            element = f'<h1 style="grid-column:{x} / span {w};grid-row:{y} / span {h};">Title</h1>'
        
        elif i["element"] == "picture":
            element = f'<div class="c-image" style="min-height:{h * 32}px;grid-column:{x} / span {w};grid-row:{y} / span {h};"></div>'
        
        elif i["element"] == "text":

            loremText = lorem.paragraphs(1)
                     
            
            element = f'<p class="c-text" style="grid-column:{x} / span {w};grid-row:{y} / span {h};">{loremText}</p>'
        

        htmlString += element + "\n"

        htmlDoc = f'<!DOCTYPE html> <html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>result</title><link rel="stylesheet" href="css/normalize.css"><link rel="stylesheet" href="https://use.typekit.net/hwf3rrs.css"><link rel="stylesheet" href="css/screen.css"></head><body><div class="o-container">    <div class="c-content o-row">{htmlString}</div></div></body></html>'

    try:
        with open(f'result-{name}/index.html', 'w') as outfile:
            outfile.write(htmlDoc)
    except Exception as e:
        print(e) 
    


 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help = "give input file to make a prediction")
    parser.add_argument("-n", "--name", help = "give name for result folder")
    args = parser.parse_args()

    # Load in model
    model = core.Model.load("model_weights_v1.pth", ["checkbox", "text","picture","heading"])

    # Get predcition for given image
    filtered_boxes, filtered_labels = predict(model, args.input)

    # Convert the prediction to 
    jsonList = prediction_to_json(filtered_boxes, filtered_labels, args.input)

    json_to_html(jsonList, args.name)



    

    


 
