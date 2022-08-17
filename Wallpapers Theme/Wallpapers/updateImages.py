import os, shutil, json, base64, time, re

validExtensions = [".jpg", ".png", ".svg", ".gif", ".jpeg"]

cssDir = "generatedCSSFiles"
b64Dir = "sharedB64Images"
fallbackCSSDir = "fallbackCSS"
autoGenHeader = "/* This File was Auto-Generated Do Not Modify */\n\n"
cssVariableTemplate = f"{autoGenHeader}:root{{\n\t--<customVarName>: var(--<imageVariableName>, radial-gradient(155.42% 100% at 0% 0%, #151f25 0 0%, #152533 100%));\n}}"
fallbackCssVariableTemplate = f"{autoGenHeader}:root{{\n\t--<customVarName>: radial-gradient(155.42% 100% at 0% 0%, #151f25 0 0%, #152533 100%) !important;\n}}"

cssFileTypes = { 
    b64Dir: f"{autoGenHeader}:root{{\n\t--<imageVariableName>: url('data:image/<imgType>;base64,<b64String>') !important;\n}}",
    fallbackCSSDir: fallbackCssVariableTemplate
}

imageCount = 0


def log(message):
    #print(message)
    pass

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

        if type == b64Dir:
            b64 = getB64ForFile(filePath)

            f = open(f"{cssDir}/{type}/{fileName}" , "w")
            tmpStr = cssFileTypes[type].replace("<imageVariableName>", variableName).replace("<b64String>", b64).replace("<imgType>", getImgTypeTagForFileExt(fileInfo[1]))
            f.write(tmpStr)
            f.close()
        elif type == fallbackCSSDir:
            f = open(f"{cssDir}/{type}/{fileName}" , "w")
            tmpStr = cssFileTypes[type].replace("<customVarName>", varName)
            f.write(tmpStr)
            f.close()
        else:
            f = open(f"{cssDir}/{type}/{fileName}" , "w")
            f.write(cssFileTypes[type].replace("<imageVariableName>", variableName))
            f.close()
    except Exception as e:
        log(f"Error  writing type {type}: {str(e)}")
        rv = False

    return rv



def main():
    global imageCount
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    if os.path.isdir(cssDir):
        shutil.rmtree(cssDir)
    
    jsonTemplate = open("themeTemplate.json")
    themeJson = json.load(jsonTemplate)
    jsonTemplate.close()
    # Create Folder Structure
    os.mkdir(cssDir)
    os.mkdir(f"{cssDir}/{b64Dir}")
    os.mkdir(f"{cssDir}/{fallbackCSSDir}")

    for k,v in themeJson["patches"].items():
        if v["type"] == "dropdown-image":
            if "css_variable" in v.keys() and re.match(r"[A-Za-z0-9_-]+", v["css_variable"]):
                tmpVar = v["css_variable"]
                log(tmpVar)
                os.mkdir(f'{cssDir}/{tmpVar}')
                cssFileTypes[v["css_variable"]] = cssVariableTemplate.replace("<customVarName>", v["css_variable"])

                if "values" in v.keys():
                    v["values"]["None"] = {f"{cssDir}/{fallbackCSSDir}/{v['css_variable']}.css": ["SP"]}
                    writeCSSType(fallbackCSSDir, "", v['css_variable'])
                if "default" in v.keys() and "None" != v["default"]:
                    v["default"] = "None"

            else:
                raise ValueError(f'Invalid css variable name')




    for root, dirs, files in os.walk("./images"):
        for file in files:
            fileInfo = os.path.splitext(file)
            if len(fileInfo) == 2 and ((fileInfo[1].lower()) in validExtensions):
                log("Creating CSS files for " + file)
                imageImportedSuccessfully = True
                imageVarName = ""
                imageVarName = imageVarName.join(e for e in fileInfo[0].lower().title() if (e.isalnum() or e.isspace()))
                imageVarName = " ".join(imageVarName.split())
                
                for cssType, cssTemplate in cssFileTypes.items():
                    if  imageImportedSuccessfully:
                        if cssType != fallbackCSSDir:
                            imageImportedSuccessfully = writeCSSType(cssType, os.path.join(root, file), imageVarName)
                
                if imageImportedSuccessfully:
                    # Update Theme.json
                    log("Success")
                    for k,v in themeJson["patches"].items():
                        if v["type"] == "dropdown-image":
                            log(f"Adding {imageVarName} for var {v['css_variable']}")
                            if "css_variable" in v.keys() and re.match(r"[A-Za-z0-9_-]+", v["css_variable"]):
                                themeJson["patches"][k]["values"][imageVarName] = { f"{cssDir}/{b64Dir}/{imageVarName}.css": ["SP"], f'{cssDir}/{v["css_variable"]}/{imageVarName}.css': ["SP"]}
                            else:
                                # No Var replace Normal dropdown Patch
                                v["type"] = "dropdown"
                    imageCount += 1

                    
                else:
                    log("Failed")

    # Sanitize Extended Types
    for k,v in themeJson["patches"].items():
        if "css_variable" in v.keys():
            del v["css_variable"]
        if "type" in v.keys() and v["type"] == "dropdown-image":
            v["type"] = "dropdown"


    f = open("theme.json" , "w")
    f.write(json.dumps(themeJson, indent=4))
    f.close()

                


if __name__ == '__main__':
    startTime = time.time()
    try:
        main()
        log("Image Import was Successful")
    except Exception as e:
        log("Error Generating CSS Files: " + str(e))

    log(f"CSS Generated for {imageCount} images in {1000 * (time.time() - startTime)} ms")
