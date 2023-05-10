# EDNA
Created by Evan Scherrer and Declan Moore


## About 
EDNA (Edible Data & Numerical Analysis) is a web app we made for our Intro to CS final project. We're aware that EDNA probably far exceeds the requirements of the project, but we also like making cool stuff and therefore don't care. 

EDNA is a web app that allows you to input the ingredients list of a recipe, modify the recipe by quantity, choose a retailer, and figure out how much the ingredients of your recipe cost. EDNA does not account for food you already have in your pantry, and it calculates prices based only on what you use. For example, four hot dogs [out of this pack of 8](https://www.target.com/p/-/A-12959588) returns a price of $1.49, even though you'd still have to buy the entire pack of hot dogs.


## Usage 
1. Enter your list of ingredients (works best without modifiers, e.g. `1 cup flour` instead of `1 cup unsifted, unbleached flour`)  
2. Enter the number of servings your recipe makes*  
3. Adjust recipe if desired  
    - by scale factor (scale to 2x for a double recipe)  
    - by servings (scale a recipe from 8 servings to 12 servings)  
    - by cost (scale a recipe up or down to a target cost)  
4. Select retailer  
5. Click `Calculate`  
6. Follow the prompts to select products  

See example with my grandma's sour cream cookies:  
![EDNA With Grandma's Sour Cream Cookies](/assets/ednaDemo.PNG)

\* only necessary if you're going to be adjusting your recipe based on the number of servings (e.g. scale a recipe that makes 8 servings up to 12 servings)


## Installation & Setup
### Windows
1. [Install Python](https://www.python.org/downloads/)  
2. [Install Node.js](https://nodejs.org/en/download)  
3. [Install Git (to clone this repo)](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)  
4. Install Node Packages  
    - ElectronJS (run the project locally); run `npm install electron -g` in a terminal  
    - Python-Shell (run python code from node.js); run `npm install python-shell` in a terminal  
5. Install Python Packages  
    - Requests (make HTTP requests for web scraping); run `pip install requests` in a terminal  
    - Beautiful Soup (parse product data from requests); run `pip install beautifulsoup4` in a terminal  
6. Download this repo (if using Git, create a directory, navigate your terminal inside that directory, and run `git clone https://github.com/Jovan-04/recipe-web-scraper.git`)  
7. Navigate your terminal into the `src` folder of this repo  
8. Run the project from the terminal with `electron app.js`  

### Mac
Probably about the same as windows. I don't have an Apple computer to try it on. If anyone wants to make a PR adding this (or one for linux), that'd be much appreciated. 


## FAQs (WIP)
**Q:** Why *sour cream* cookies in the usage guide?!?  
**A:** They're better than you think.  

**Q:** Why doesn't the product actually tell me how much I need to buy, and what *that* will cost me?  
**A:** Because that's much more complicated, this is a prototype, we only spent about 6-8 weeks working on this, and we didn't feel like it.  