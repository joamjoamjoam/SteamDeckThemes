import os, shutil

validExtensions = [".jpg", ".png", ".svg", ".gif"]
cssDir = "generatedCSSFiles"
lockScreenCssDir = "lockscreen"
homeScreenCssDir = "homescreen"
libraryCssDir = "library"

def main():
    print("In Main")
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    print("Working in ", os.getcwd())

    if os.path.isdir(cssDir):
        shutil.rmtree(cssDir)

    for root, dirs, files in os.walk("."):
        for file in files:
            fileInfo = os.path.splitext(file)
            if len(fileInfo) == 2 and ((fileInfo[1].lower()) in validExtensions):
                print("Creating CSS for " + file)
                


if __name__ == '__main__':
    main()