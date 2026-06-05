from PIL import Image

def make_transparent(img_path):
    img = Image.open(img_path).convert("RGBA")
    datas = img.getdata()
    
    newData = []
    for item in datas:
        # Get the intensity of the pixel (closer to 0 is black)
        # We can use the RGB values to set the alpha channel.
        # If it's mostly black, it becomes transparent.
        # Cyan is (6, 182, 212) -> (R, G, B)
        # We can use the max of R, G, B as the alpha channel, and set the color to pure cyan (or keep original color).
        
        # Calculate brightness/luminance
        brightness = max(item[0], item[1], item[2])
        
        # If it's very dark, make it completely transparent
        if brightness < 20:
            newData.append((0, 0, 0, 0))
        else:
            # Keep the color, but scale alpha based on brightness to ensure smooth edges
            # Map brightness 20-255 to alpha 0-255
            alpha = int(((brightness - 20) / 235.0) * 255)
            newData.append((item[0], item[1], item[2], alpha))
            
    img.putdata(newData)
    img.save("frontend/logo.png", "PNG")

make_transparent("frontend/logo.png")
