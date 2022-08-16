import os, shutil, json, base64, time

validExtensions = [".jpg", ".png", ".svg", ".gif", ".jpeg"]

cssDir = "generatedCSSFiles"
lockScreenCssDir = "lockscreen"
homeScreenCssDir = "homescreen"
libraryCssDir = "library"
keyboardCssDir = "keyboard"
b64Dir = "sharedB64Images"
lockScreenVarName = "--WPRLockScreenWallPaper"
homeScreenVarName = "--WPRHomeScreenWallPaper"
libraryVarName = "--WPRLibraryWallPaper"
keyboardVarName = "--WPRKeyboardWallPaper"

# Main CSS File paths
lockScreenMainPath = "wallpaperCSS/lockScreen.css"
homeScreenMainPath = "wallpaperCSS/homeScreen.css"
libraryMainPath = "wallpaperCSS/library.css"
keyboardMainPath = "wallpaperCSS/keyboard.css"

cssFileTypes = { 
    b64Dir: f":root{{\n\t<variableName>: url('data:image/<imgType>;base64,<b64String>') !important;\n}}", \
    lockScreenCssDir: f":root{{\n\t{lockScreenVarName}: var(<variableName>);\n}}", \
    homeScreenCssDir: f":root{{\n\t{homeScreenVarName}: var(<variableName>);\n}}", \
    libraryCssDir: f":root{{\n\t{libraryVarName}: var(<variableName>);\n}}", \
    keyboardCssDir: f":root{{\n\t{keyboardVarName}: var(<variableName>);\n}}" \
}

exitTimeout = 5


themeJsonBase = "{ \"name\": \"Wallpapers\", \"version\": \"v1.0\", \"author\": \"joamjoamjoam\", \"target\": \"System-Wide\", \"description\": \"Sets Wallpapers. What did you Expect?\", \"manifest_version\": 2, \"inject\": { }, \"patches\": {  \"Disable Home Overlay\": { \"default\": \"Yes\", \"type\": \"dropdown\", \"values\" : { \"No\" : {}, \"Yes\" : { \"homeScreenOverlay/disabled.css\" : [ \"SP\" ] } } }, \"Home Screen Image\": { \"default\": \"None\", \"type\": \"dropdown\", \"values\":{ \"None\": {} } }, \"Lock Screen Image\": { \"default\": \"None\", \"type\": \"dropdown\", \"values\":{ \"None\": {} } }, \"Library Background Image\": { \"default\": \"None\", \"type\": \"dropdown\", \"values\":{ \"None\": {} } }, \"Keyboard Background Image\": { \"default\": \"None\", \"type\": \"dropdown\", \"values\":{ \"None\": {} } } } }"

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
        
        variableName = "--WPRImage" + varName.replace(" ", "")

        if type == "sharedB64Images":
            b64 = getB64ForFile(filePath)

            f = open(f"{cssDir}/{type}/{fileName}" , "w")
            tmpStr = cssFileTypes[type].replace("<variableName>", variableName).replace("<b64String>", b64).replace("<imgType>", getImgTypeTagForFileExt(fileInfo[1]))
            f.write(tmpStr)
            f.close()
        else:
            f = open(f"{cssDir}/{type}/{fileName}" , "w")
            f.write(cssFileTypes[type].replace("<variableName>", variableName))
            f.close()
    except Exception as e:
        print(f"Error  writing type {type}: {str(e)}")
        rv = False

    return rv



def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    if os.path.isdir(cssDir):
        shutil.rmtree(cssDir)
    
    # Create Folder Structure
    os.mkdir(cssDir)
    os.mkdir(cssDir + "/" + lockScreenCssDir)
    os.mkdir(cssDir + "/" + homeScreenCssDir)
    os.mkdir(cssDir + "/" + libraryCssDir)
    os.mkdir(cssDir + "/" + b64Dir)
    os.mkdir(cssDir + "/" + keyboardCssDir)

    themeJson = json.loads(themeJsonBase)

    for root, dirs, files in os.walk("./images"):
        for file in files:
            fileInfo = os.path.splitext(file)
            if len(fileInfo) == 2 and ((fileInfo[1].lower()) in validExtensions):
                print("Creating CSS files for " + file)
                imageImportedSuccessfully = True
                varName = ""
                varName = varName.join(e for e in fileInfo[0].lower().title() if (e.isalnum() or e.isspace()))
                varName = " ".join(varName.split())
                for cssType, cssTemplate in cssFileTypes.items():
                    if  imageImportedSuccessfully:
                       imageImportedSuccessfully = writeCSSType(cssType, os.path.join(root, file), varName)
                
                if imageImportedSuccessfully:
                    # Update Theme.json
                    print("Success")
                    themeJson["patches"]["Home Screen Image"]["values"][varName] = { f"{cssDir}/{b64Dir}/{varName}.css": ["SP"], f"{cssDir}/{homeScreenCssDir}/{varName}.css": ["SP"], f"{homeScreenMainPath}": ["SP"]}
                    themeJson["patches"]["Lock Screen Image"]["values"][varName] = { f"{cssDir}/{b64Dir}/{varName}.css": ["SP"], f"{cssDir}/{lockScreenCssDir}/{varName}.css": ["SP"], f"{lockScreenMainPath}": ["SP"]}
                    themeJson["patches"]["Library Background Image"]["values"][varName] = { f"{cssDir}/{b64Dir}/{varName}.css": ["SP"], f"{cssDir}/{libraryCssDir}/{varName}.css": ["SP"], f"{libraryMainPath}": ["SP"]}
                    themeJson["patches"]["Keyboard Background Image"]["values"][varName] = { f"{cssDir}/{b64Dir}/{varName}.css": ["SP"], f"{cssDir}/{keyboardCssDir}/{varName}.css": ["SP"], f"{keyboardMainPath}": ["SP"]}
                else:
                    print("Failed")
    
    #print(json.dumps(themeJson, indent=4))

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
