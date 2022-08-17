import os, shutil, json, base64, time, re

validExtensions = [".jpg", ".png", ".svg", ".gif", ".jpeg"]

cssDir = "generatedCSSFiles"
b64Dir = "sharedB64Images"
cssVariableTemplate = f":root{{\n\t--<customVarName>: var(--<imageVariableName>);\n}}"

cssFileTypes = { 
    b64Dir: f":root{{\n\t--<imageVariableName>: url('data:image/<imgType>;base64,<b64String>') !important;\n}}"
}

exitTimeout = 5

def getB64ForFile(file):
    rv = ""
    try:
        if os.path.exists(file):
            with open(file, "rb") as image_file:
                raw = base64.b64encode(image_file.read())
                rv = raw.decode('utf-8')
    except:
        pass
    
    return rv

def getImgTypeTagForFileExt(fileExt):
    rv = "jpeg"
    fileExt = fileExt.lower()

    if fileExt in validExtensions:
        if fileExt == ".jpg" or fileExt == ".jpeg":
            rv = "jpeg"
        elif fileExt == ".svg":
            rv = "svg+xml"
        elif fileExt == ".gif":
            rv = "gif"
        elif fileExt == ".png":
            rv = "png" 

    else:
        rv = "jpeg"

    return rv

def writeCSSType(type, filePath, varName):

    rv = True

    fileInfo = os.path.splitext(os.path.basename(filePath))
    

    try:
        if not type in cssFileTypes.keys() or len(fileInfo) != 2:
            raise ValueError("Not a Valid type or image path") 
        
        fileName = f"{varName}.css"
        
        variableName = "WPRImage" + varName.replace(" ", "")

        if type == "sharedB64Images":
            b64 = getB64ForFile(filePath)

            f = open(f"{cssDir}/{type}/{fileName}" , "w")
            tmpStr = cssFileTypes[type].replace("<imageVariableName>", variableName).replace("<b64String>", b64).replace("<imgType>", getImgTypeTagForFileExt(fileInfo[1]))
            f.write(tmpStr)
            f.close()
        else:
            f = open(f"{cssDir}/{type}/{fileName}" , "w")
            f.write(cssFileTypes[type].replace("<imageVariableName>", variableName))
            f.close()
    except Exception as e:
        print(f"Error  writing type {type}: {str(e)}")
        rv = False

    return rv



def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    if os.path.isdir(cssDir):
        shutil.rmtree(cssDir)
    
    jsonTemplate = open("themeTemplate.json")
    themeJson = json.load(jsonTemplate)
    jsonTemplate.close()
    # Create Folder Structure
    os.mkdir(cssDir)
    os.mkdir(f"{cssDir}/{b64Dir}")

    for k,v in themeJson["patches"].items():
        if v["type"] == "dropdown-image":
            if "var" in v.keys() and re.match(r"[A-Za-z0-9_-]+", v["var"]):
                tmpVar = v["var"]
                print(tmpVar)
                os.mkdir(f'{cssDir}/{tmpVar}')
                cssFileTypes[v["var"]] = cssVariableTemplate.replace("<customVarName>", v["var"])
                print(cssFileTypes)
            else:
                raise ValueError(f'Invalid css variable name')




    for root, dirs, files in os.walk("./images"):
        for file in files:
            fileInfo = os.path.splitext(file)
            if len(fileInfo) == 2 and ((fileInfo[1].lower()) in validExtensions):
                print("Creating CSS files for " + file)
                imageImportedSuccessfully = True
                imageVarName = ""
                imageVarName = imageVarName.join(e for e in fileInfo[0].lower().title() if (e.isalnum() or e.isspace()))
                imageVarName = " ".join(imageVarName.split())
                
                for cssType, cssTemplate in cssFileTypes.items():
                    if  imageImportedSuccessfully:
                       imageImportedSuccessfully = writeCSSType(cssType, os.path.join(root, file), imageVarName)
                
                if imageImportedSuccessfully:
                    # Update Theme.json
                    print("Success")
                    for k,v in themeJson["patches"].items():
                        if v["type"] == "dropdown-image":
                            print(f"Adding {imageVarName} for var {v['var']}")
                            if "var" in v.keys() and re.match(r"[A-Za-z0-9_-]+", v["var"]):
                                themeJson["patches"][k]["values"][imageVarName] = { f"{cssDir}/{b64Dir}/{imageVarName}.css": ["SP"], f'{cssDir}/{v["var"]}/{imageVarName}.css': ["SP"]}
                            else:
                                # No Var replace Normal dropdown Patch
                                v["type"] = "dropdown"

                    
                else:
                    print("Failed")
    
    #print(json.dumps(themeJson, indent=4))

    # Sanitize Extended Types
    for k,v in themeJson["patches"].items():
        if "var" in v.keys():
            del v["var"]
        if "type" in v.keys() and v["type"] == "dropdown-image":
            v["type"] = "dropdown"


    f = open("theme.json" , "w")
    f.write(json.dumps(themeJson, indent=4))
    f.close()

                


if __name__ == '__main__':
    try:
        main()
        print("Image Import was Successful")
    except Exception as e:
        print("Error Generating CSS Files: " + str(e))
    
    for i in range(0, exitTimeout):
        print(f"Exiting in {exitTimeout - i} seconds ...")
        time.sleep(1)
