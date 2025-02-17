# VT Hunt Logo Maker
<strong>Generates [VT Hunt](https://www.vthunt.com/) logos as .pngs for any given font.</strong>
<br>------------------------------------------------------------<br>
[Files in this repository](https://github.com/sagudelis/logo-generator/edit/main/README.md#files-in-this-repository)<br>
[How to use the logo maker](https://github.com/sagudelis/logo-generator/edit/main/README.md#using-the-logo-maker-standalone-file)<br>
[Necessary installations](https://github.com/sagudelis/logo-generator/edit/main/README.md#necessary-installations)

## Files in this repository
[logomaker.py](https://github.com/sagudelis/logo-generator/blob/main/logomaker.py) is a standalone file with a command line interface that can be run in python.<br>
[logomakerbot.py](https://github.com/sagudelis/logo-generator/blob/main/logomakerbot.py) is written to be used within a discord bot.

## Using the logo maker standalone file 
When the file is run, it will prompt the user for three inputs:<br>
1. A source for the desired font. See more about choosing fonts [here](https://github.com/sagudelis/logo-generator/edit/main/README.md#what-the-font).
2. A color choice in RGBA format. If this field is left blank or the given input is invalid, it will default to white (255, 255, 255, 255).
3. A symmetry boolean that says whether or not the VT should be horizontally mirrored, as a yes or no answer. If this field is left blank or the given input is invalid, it will default to true. See more about what symmetry means [here](https://github.com/sagudelis/logo-generator/edit/main/README.md#symmetry).

Here's an example of what the CLI may look like and the image it generates:
><img src="https://github.com/user-attachments/assets/b7a892c4-d78b-4f2b-9f6b-295cc765d0f3" alt="cli example logo" width="75%">
><img src="https://github.com/user-attachments/assets/2b0680d4-32fb-4900-a7f9-965b9ef40364" alt="generated logo" width="30%">


### Inputting Fonts
Fonts can be input in two formats: 
1. As a [URL to a download link](https://github.com/sagudelis/logo-generator/edit/main/README.md#as-a-url) for a file.
2. As a [path to a zip file](https://github.com/sagudelis/logo-generator/edit/main/README.md#as-a-zip-file).

#### As a URL
On any font website, find a font you want to use. Find the download button for the desired font, and copy the link to this button. Here are two examples of what this might look like:<br> 
>![image](https://github.com/user-attachments/assets/0159d4da-04ad-477a-93b0-d2b3f88442b9)
>![image](https://github.com/user-attachments/assets/5c1ad5b6-fdaa-44d0-ab28-76df45ee477e)

Once you've copied this link, you can paste it into the command line when prompted for a download URL or zip file and the font will be used to generate your logo!<br>


#### As a zip file
If there is a font that you cannot copy the download link to, or if you want to use a font you have saved locally, you can use the path of the zip file containing that font to use it!<br><br> 
Here's an example of what that may look like in the command line:
><img src="https://github.com/user-attachments/assets/ffbaecfd-d69c-451d-a9f7-2429f97c7598" alt="cli example zip file" width="75%"><br>
>*Note: The code will automatically strip any quotation marks, but it is best to input the path without them*


### Symmetry
The symmetry boolean is used to determine if the VT should be mirrored horizontally or not. Below are two examples of logos generated with and without symmetry, using the same font. 
> Generated with symmetry:<br>
> <img src="https://github.com/user-attachments/assets/9fc2f948-df15-463d-856d-fcbeb3a3682f" alt="with symmetry" width="50%"><br>
> <br><br>
> Generated without symmetry:<br>
> <img src="https://github.com/user-attachments/assets/dfb9c6ca-39d9-4dd9-9376-1ac272b2501e" alt="without symmetry" width="50%"><br>

### Necessary installations
The standalone python file uses several packages outside of Python's standard library. To make sure everything runs properly, please install the following packages before running the program:
- [Requests](https://requests.readthedocs.io/en/latest/)
- [Pillow](https://pypi.org/project/pillow/) 


