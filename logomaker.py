import io
import os
import requests
import discord
import warnings
from zipfile import ZipFile
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from discord import app_commands

path = './'
# stop the deprecation warning from popping up
warnings.filterwarnings('ignore')

def text_to_image(text: str, font_filepath: str, font_size: int, color: tuple) -> Image:
    try:
        font = ImageFont.truetype(font_filepath, size=font_size)
    except Exception as e:
        print(f"Error loading font {font_filepath}: {e}")
        return None

    # Create a dummy image to get the size of the text
    dummy_img = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=font)  # Get the bounding box of the text
    size = (bbox[2] - bbox[0], bbox[3] - bbox[1])

    # Create the actual image with the proper size
    img = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.text((-bbox[0], -bbox[1]), text, fill=color, font=font)  # Adjust the position according to the bounding box

    return img

# function to merge two images
def imageMerger(images, h_or_v, gap_os=0):
    gap_os = round(gap_os/2)

    # get height and width of image canvas
    newImW = 0
    newImH = 0
    for image in images:
        if 'h' in h_or_v:
            newImW += image.size[0]
            if image.size[1] > newImH:
                newImH = image.size[1]
        if 'v' in h_or_v:
            newImH += image.size[1]
            if image.size[0] > newImW:
                newImW = image.size[0]

    # add padding to make sure images are all same size - for centering
    for idx, image in enumerate(images):
        if 'h' in h_or_v:
            if image.size[1] < newImH:
                hToAdd = round((newImH - image.size[1])/2)
                new_h = image.size[1] + hToAdd + hToAdd
                paddedIm = Image.new(image.mode, (image.size[0], new_h), (255, 255, 255, 0))
                paddedIm.paste(image, (0, hToAdd))
                images[idx] = paddedIm
        if 'v' in h_or_v:
            if image.size[0] < newImW:
                wToAdd = round((newImW - image.size[0])/2)
                new_w = image.size[0] + wToAdd + wToAdd
                paddedIm = Image.new(image.mode, (new_w, image.size[1]), (255, 255, 255, 0))
                paddedIm.paste(image, (wToAdd, 0))
                images[idx] = paddedIm

    new_image = Image.new('RGBA', (newImW, newImH), (255, 255, 255, 0))

    curImW = 0
    curImH = 0
    for idx, image in enumerate(images):
        new_image.paste(image, (curImW, curImH), image)

        if 'h' in h_or_v:
            curImW += image.size[0] - gap_os
        if 'v' in h_or_v:
            curImH += image.size[1] - gap_os

    text_window = new_image.getbbox()
    new_image = new_image.crop(text_window)

    return new_image

# function to find the skinniest part of the top of the T
def getTHeight(tImg):
    # gets max height of left 1/4 of image
    # t.crop(tuple((0, 0, round(t.size[0] / 4), t.size[1]))).getbbox()[3]

    # get the narrowest part of upper half of the image
    uhFull = tImg.crop(tuple((0, 0, tImg.size[0], round(tImg.size[1]/2))))    # get whole upper half image
    uhFull = uhFull.crop(uhFull.getbbox())  # trim to bounding box
    edgeSize = round(uhFull.size[0]/10)     # get size of edges to trim off
    upperHalf = uhFull.crop(tuple((edgeSize, 0, uhFull.size[0]-edgeSize, uhFull.size[1])))

    narrowest = tImg.size[1]
    for vSliceInt in range(upperHalf.size[0]-1):      # for each row of pixel
        # make the single pixel vertical slice
        vSlice = upperHalf.crop(tuple((vSliceInt, 0, vSliceInt+1, upperHalf.size[1])))
        # get the bounding box for the single pixel vertical slice
        bounds = vSlice.getbbox()
        if bounds is not None:
            boxHeight = bounds[3] - bounds[1]    # the height of the bounding box
            if boxHeight < narrowest:
                narrowest = boxHeight

    # print(f'theight is {narrowest}')
    return narrowest

# function to remove edges from image and optionally color
def colorImage(image, color, trans):
    colorNew = color + tuple((0,))
    image.load()
    A = image.getchannel('A')
    # Make all opaque pixels into semi-opaque
    alpha = A.point(lambda i: trans if i > 0 else 0)
    image2 = Image.new(image.mode, image.size, colorNew)
    image2.putalpha(alpha)
    newImg = image2.filter(ImageFilter.SMOOTH)

    return newImg


def makeTheLogo(url=None, file=None, RGBA="(255,255,255,255)", symmetry=True):
    path = './fonts'
    if not os.path.exists(path):
        os.makedirs(path)
    
    try:
        R, G, B, A = map(int, RGBA.replace('(', '').replace(')', '').split(','))
        userColor = tuple((R, G, B))
    except:
        userColor = tuple((255, 255, 255))
        A = 255
    userTrans = A
    allFonts = []
    fontNames = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive'
    }
    
    if url:
        response = requests.get(url, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            content_type = response.headers['Content-Type']
            if 'font' in content_type or url.lower().endswith(('.otf', '.ttf')):
                font_name = os.path.basename(url)
                font_path = os.path.join(path, font_name)
                with open(font_path, 'wb') as f:
                    f.write(response.content)
                allFonts.append(font_path)
                fontNames.append(font_name.split('.')[0])
            else:
                file_like_object = io.BytesIO(response.content)
                try:
                    with ZipFile(file_like_object) as zf:
                        for file in zf.namelist():
                            if file.lower().endswith('.otf') or file.lower().endswith('.ttf'):
                                zf.extract(file, path)
                                fpath = os.path.join(path, file)
                                allFonts.append(fpath)
                                fontNames.append(file.split('/')[-1].split('.')[0])
                except Exception as e:
                    print(f"Error processing zip file: {e}")
        else:
            print(f"Error downloading URL: {response.status_code}")
    elif file:
        file_like_object = file
    
    if file:
        try:
            with ZipFile(file_like_object) as zf:
                for file_info in zf.infolist():
                    file_name = file_info.filename
                    if file_name.lower().endswith('.otf') or file_name.lower().endswith('.ttf'):
                        zf.extract(file_name, path)
                        fpath = os.path.join(path, file_name)
                        allFonts.append(fpath)
                        fontNames.append(file_name.split('/')[-1].split('.')[0])
        except Exception as e:
            print(f"Error processing zip file: {e}")
    
    allLogos = []
    for idx, font in enumerate(allFonts):
        try:
            v = text_to_image(text='V', font_filepath=font, font_size=1000, color=tuple((255, 255, 255, 255)))
            t = text_to_image(text='T', font_filepath=font, font_size=1000, color=tuple((255, 255, 255, 255)))
            if v is None or t is None:
                print(f"Skipping font {fontNames[idx]} due to previous error.")
                continue
            tHeight = getTHeight(tImg=t)
            vcrop = v.crop(tuple((0, round(tHeight/2), v.size[0], v.size[1])))
            v = vcrop

            # Upper left
            vm = ImageOps.flip(v)
            tm = ImageOps.flip(t)

            # Upper right
            v_upper_right = ImageOps.mirror(vm) if symmetry else vm
            t_upper_right = ImageOps.mirror(tm) if symmetry else tm

            # Bottom left
            v_bottom_left = v.copy()
            t_bottom_left = t.copy()

            # Bottom right
            v_bottom_right = ImageOps.mirror(v) if symmetry else v
            t_bottom_right = ImageOps.mirror(t) if symmetry else t

            dbv = imageMerger([vm, v], 'vertical', gap_os=0)
            dbt = imageMerger([tm, t], 'vertical', gap_os=round(tHeight*2))
            dbv_right = imageMerger([v_upper_right, v_bottom_right], 'vertical', gap_os=0)
            dbt_right = imageMerger([t_upper_right, t_bottom_right], 'vertical', gap_os=round(tHeight*2))

            logo = imageMerger([dbv, dbt, dbt_right, dbv_right], 'horizontal', gap_os=tHeight)
            logo = colorImage(logo, userColor, userTrans)
            name = f'./logos/logo{idx}.png'
            logo.save(name)
            allLogos.append(name)
        except Exception as e:
            print(f'Error with {fontNames[idx]} font: {e}')
    
    return allLogos

def make_logo_command(tree: app_commands.CommandTree):

    @tree.command(name="logoho", description="Create a logo from a URL or an uploaded font file")
    @app_commands.describe(url="URL of the zip file containing fonts or a direct font file (optional)", file="Uploaded font file (optional)", rgba="RGBA color format", symmetry="Whether the V and T should be mirrored (optional, defaults to true)")
    async def make_logo(interaction: discord.Interaction, rgba: str = "(255,255,255,255)", url: str = None, file: discord.Attachment = None, symmetry: bool = True):
        if not url and not file:
            await interaction.response.send_message("You must provide either a URL or upload a font file.", ephemeral=True)
            return

        if url and file:
            await interaction.response.send_message("Please provide only one input, either a URL or a font file.", ephemeral=True)
            return

        try:
            if url:
                logos = makeTheLogo(url=url, RGBA=rgba, symmetry=symmetry)
            elif file:
                font_bytes = await file.read()
                file_like_object = io.BytesIO(font_bytes)
                logos = makeTheLogo(file=file_like_object, RGBA=rgba, symmetry=symmetry)

            await interaction.response.send_message("Logos generated successfully. Sending files...", ephemeral=True)
            
            for logofile in logos:
                with open(logofile, 'rb') as f:
                    await interaction.followup.send(file=discord.File(f))
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)
