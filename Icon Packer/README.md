# Icon Packer

## Applies System-Wide Icon Packs. Add your own by following the Xbox Icon Pack template.

### Requirements
- Install Decky Loader Plugin Manager
- Install CSSLoader plugin from the Decky Loader Plugin Store.

### Icon Sizes
- All Icons should be 32px x 32px
- Steam Button Icon should be 100px x 36px

### Creating your own Icon Pack

1. Copy the Xbox Icon Pack as a template
2. Place your icons of the proper size into the ThemeName/icons Folder
3. Replace the image paths in your packs Icon.css to match your icons
4. Add your Icon Pack to the dropdown menu in theme.json
5. Update the path to your themes Icons.css file in the theme.json
6. (Optional) Submit the icon pack following the pricedure mentioned below.
7. (Optional) To test icons locally copy the Enite Icon Packer folder to /home/deck/homebrew/themes folder and reload themes using the CSSLoader Plugin UI.
 
 ### Icon Pack Folder Structure
├── Icon Sets
│   └── Theme Name
│       ├── icons (folder containing your icons)
│       │   └── icon.png
│       └── Icons.css (Use the Xbox theme as a template to set the paths to your icon images)
│       └── README.md (README to show images/describe icon pack. Can use the root /images directory to hold the images. Credit All Images if needed.)
├── ICPShared.css
└── theme.json (Add your theme to the dropdown box. Optionally add your name to the Authors field)

## Submission
- Feel free top submit PRs for your Icon Packs and Ill update the theme on the CSS Loader Store to include it.
- Images must follow the guidelines of the CSS Loder store. No NSFW or violent content.
- Update the theme.json to include your theme. Follow the Xbox icon pack as a template.
- Submit a PR to this repository
- Credit All Images you do not own in your icon pack README.

### Disclaimer: I do not own any of the images in this repository. If you are the owner and would like to remove an image or icon pack please submit a github issue and it will be taken down.

