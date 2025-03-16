![Logo](https://raw.githubusercontent.com/padmanabhpvdev/DeepSeaView/refs/heads/main/enhancer/static/images/gitlogo.png)
# DeepSeaView
An advanced image enhancement system designed to improve the clarity and quality of underwater visuals using Discrete Cosine Transform.
## Overview
Underwater images often suffer from poor visibility due to light absorption, scattering and color distortion.
**DeepSeaView** is an advanced image enhancement system designed to improve the clarity and quality of underwater visuals using Discrete Cosine Transform (DCT). By leveraging the frequency-domain properties of DCT, the system effectively reduces noise, enhances contrast and restores color balance in submerged environments. This approach enables better feature extraction and visibility, making it ideal for marine research, underwater photography and robotic vision applications.
DeepSeaView enhances image details while preserving natural textures, ensuring a more accurate and visually appealing representation of underwater scenes.
## Requirements
- Windows 10 or later
- Python 3.x or later
- Any Web Browser
- VSCode or any code editors
## Installation
Download the source code using Git Clone:
```bash
git clone https://github.com/padmanabhpvdev/DeepSeaView.git
```
Or download it in zip format and unzip it!

Next,open Command Prompt or Powershell and Enter into the directory using cd command:
```bash
cd DeepSeaView
```

Install the required libraries using the following command:
```bash
pip install -r requirements.txt
```

After installation is finished, step to migrate server using following command:
```bash
python manage.py migrate
```
After successful migration, run the program server using:
```bash
python manage.py runserver
```
The development server will starts. 
Open any webbrowser and paste the link given in terminal. That's it!
