from PIL import Image
def analyzeFile(file):
    if file == None:
        print("No file specified")
    
    image = Image.open(file)
    filename = image.filename
    width, height = image.size
    is_grayscale = isGrayscale(image)
    file_size = file.size
    print(f"The file name is {filename}")
    print(f"The image size is: {width}x{height} and file size is {file_size} bytes")
    print(f"The image is grayscale: {is_grayscale}")
    return {
        'filename':filename,
        'width': width,
        'height': height,
        'file_size': file_size,
        'is_grayscale': is_grayscale
    }

def isGrayscale(img):
    img = img.convert("RGB")
    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i,j))
            if r != g != b: 
                return False
    return True