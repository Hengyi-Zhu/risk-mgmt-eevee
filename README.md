# Risk Calculation Engine

The repository contains the final project for Columbia MAFN MATHGR5320 Financial Risk Management & Regulation by group Eevee (Hengyi Zhu, Shuran Zhang, Yizong Chen).

The web application is deployed [!!!here!!!](http://risk-mgmt-eevee.herokuapp.com/index) on Heroku and built with [Flask](http://flask.pocoo.org/). 

## Contents on the repository
- `inputs` folder stores data used during the development process in the `Development.ipynb`.
- `outputs` folder stores the generated csv data file when people plot using the website, as well as a default file for people to download if they click on "Download Result Data" without first ploting a graph. 
- `static` folder contains files to be loaded into the website, such as css and js files. 
- `templates` folder contains the HTML codes for the website. [Bootstrap](http://getbootstrap.com/) and javascript are used.
- `Development.ipynb` is a Jupyter Notebook file for Python 2.7. The majority of prototyping and developing was done here.
- `Documentation.txt` is the documentation for the project.
- `Procfile` and `runtime.txt` contain some default settings.
- `README.md` is what you are looking at right now.
- `app.py` is the back-end python file powering the website. It organizes the methods developed in `Development.ipynb` and communicates with the HTML. 
- `conda-requirements.txt` and `requirements.txt` contain the required python packages. Important. 
- `project_guideline.pdf` is a description of the project from the professor of this class.
