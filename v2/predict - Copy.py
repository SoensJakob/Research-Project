from detecto import core, utils, visualize
from detecto.visualize import show_labeled_image, plot_prediction_grid
from lorem_text import lorem
from sklearn import naive_bayes
import torch
import numpy as np
import json, itertools, argparse, os
import shutil, PIL


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
    thresh = 0.8
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

def get_html_element(item, containerWidth, containerHeight):
    

    gridamountX = int(containerWidth / 20 )
    gridamountY = int(containerHeight / 20 )

    x = round((item['Xmin'] / gridamountX)) + 1
    y = round((item['Ymin'] / gridamountY)) + 1

    w = round(((item["Xmax"] - item["Xmin"]) / gridamountX))
    h = round(((item["Ymax"] - item["Ymin"]) / gridamountY))

    if item["element"] == "nav":
        element = f'<div class="c-app__topbar js-nav" style="grid-column:{x} / span {w};"> <div class="c-app__mobile-nav js-nav-btn"><svg class="c-app__nav-button" xmlns="http://www.w3.org/2000/svg" width="18" height="16" viewBox="0 0 18 16"><g id="SideMenu" transform="translate(-21.5 -26.5)"><g id="Group_6" data-name="Group 6" transform="translate(21.5 27.5)"><line id="Line_1" data-name="Line 1" x2="18" fill="none" stroke="#333" stroke-width="2"/><line id="Line_2" data-name="Line 2" x2="10" transform="translate(4 7)" fill="none" stroke="#333" stroke-width="2"/><line id="Line_3" data-name="Line 3" x2="18" transform="translate(0 14)" fill="none" stroke="#333" stroke-width="2"/></g></g></svg></div>  <div class="c-app__nav"><nav class="c-nav"><ul class="o-list c-nav__list js-nav-list"><a href="#about" class="c-nav__link"><li class="c-nav__item">About</li></a><a href="#experience" class="c-nav__link"><li class="c-nav__item">Experience</li></a><a href="#projects" class="c-nav__link"><li class="c-nav__item">Projects</li></a><a href="#contact" class="c-nav__link"><li class="c-nav__item">Contact    </li></a>  </ul></nav></div></div>'
        
    elif item['element'] == "input":
        element = f'<div class="c-input" style="grid-column:{x} / span {w};grid-row:{y} / span {h};"><input type="text" /></div>'
    
    elif item["element"] == "checkbox":
        element = f'<div class="c-checkbox" style="grid-column:{x} / span {w};grid-row:{y} / span {h};"><label class="switch"> <input type="checkbox"><span class="slider round"></span></label></div>'
    
    elif item["element"] == "heading":
        element = f'<h1 class="c-heading" style="grid-column:{x} / span {w};grid-row:{y} / span {h};">Title</h1>'
    
    elif item["element"] == "frame":
        element = f'<div class="c-frame" style="min-height:{h * gridamountY / 2}px;min-width:{w * gridamountX / 4}px;grid-column:{x} / span {w};grid-row:{y} / span {h};"></div>'
    
    elif item["element"] == "text":
        loremText = lorem.paragraphs(1)
        element = f'<div class="c-text" style="max-height:{h * 128}px;max-width:{w * 64}px;grid-column:{x} / span {w};grid-row:{y} / span {h};"><p>{loremText}</p></div>'
    
    elif item['element'] == "button":
        element = f'<a href="#" class="c-nav__link c-button" style="max-width:164px;grid-column:{x} / span {w};grid-row:{y} / span {h};">Button</a>'

    elif item['element'] == "footer":
        element = f'<div class="c-footer" style="max-height:{h * gridamountY}px;grid-column:{x} / span {w};"> <p>footer</p></div>'
    
    else:
        return ""
    
    return element

def json_to_html(elementDict, width, height, name="0"):

    gridamountX = int(width / 20)
    gridamountY = int(height / 20)

    try: 
        shutil.copytree("placeholder", f"result-{name}") 

    except Exception as e: 
        print(e)  

    htmlString = ""

    Y_priority = sorted(elementDict, key=lambda d: d['Ymin'])

    in_container = []

    htmlContainer = ""

    for i in Y_priority:
        
        if i["element"] == "container":

            x = round((i['Xmin'] / gridamountX)) + 1
            y = round((i['Ymin'] / gridamountY)) + 1

            w = round(((i["Xmax"] - i["Xmin"]) / gridamountX))
            h = round(((i["Ymax"] - i["Ymin"]) / gridamountY))

            trueWidth = round(i["Xmax"] - i["Xmin"])
            trueHeight= round(i["Ymax"] - i["Ymin"])

            new_list = Y_priority.copy()
            new_list.remove(i)
            
            container = f'<div class="c-container" style="grid-column:{x} / span {w};">\n'

            for j in new_list:

                elementWidth = (j["Xmax"] - j['Xmin']) 
                elementHeight = (j["Ymax"] - j['Ymin']) 

                if (i["Xmin"] <= (j['Xmax'] - (elementWidth / 2)) <= i["Xmax"] and (i["Ymin"] <= (j['Ymax'] - (elementHeight / 2)) <= i["Ymax"])):
                    Y_priority.remove(j)
                    in_container.append(j)

                    container += get_html_element(j, trueWidth, trueHeight) + "\n"
            htmlContainer += container + "</div>\n"    
    
    htmlString = ""
    added = False
    for i in Y_priority:
        
        if i["element"] == "container" and  added == False:
            htmlString += htmlContainer + "\n"
            added = True
        else:
            htmlString += get_html_element(i, width, height) + "\n"

        htmlDoc = f'<!DOCTYPE html> <html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>result</title><link rel="stylesheet" href="css/normalize.css"><link rel="stylesheet" href="https://use.typekit.net/hwf3rrs.css"><link rel="stylesheet" href="css/screen.css"><script src="script/app.js"></script></head><body><div class="o-container">    <div class="c-content o-row">{htmlString}</div></div></body></html>'
    
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
    model = core.Model.load("model_weights_v2.pth", ["nav","frame","heading","text","checkbox","input","button","container","footer"])

    # Get predcition for given image
    filtered_boxes, filtered_labels = predict(model, args.input)

    # Convert the prediction to 
    jsonList = prediction_to_json(filtered_boxes, filtered_labels, args.input)

    image = PIL.Image.open(args.input)

    width, height = image.size

    json_to_html(jsonList, width, height, args.name)



    

    


 
