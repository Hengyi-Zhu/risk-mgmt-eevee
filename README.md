# Flask on Heroku

The repository contains a basic template for a Flask configuration that will work on Heroku.

An [example](https://lemurian.herokuapp.com) that demonstrates some basic functionality.
Another more detailed [example](https://github.com/Hengyi-Zhu/nyc-taxi) that shows how to set up 
static and templates folder, as well as path in .py files, using styles from Bootstrap.

## Step 1: Setup and deploy
- Git clone the existing template repository. `git clone <repository url on Github>`
- `Procfile`, `requirements.txt`, `conda-requirements.txt`, and `runtime.txt`
  contain some default settings.
- 'nomkl' in `conda-requirements.txt` prevents some slug size problem when deploying to heroku, 
  as it will use the non-mkl optimized binaries, and won't download the mkl package.
- There is some boilerplate HTML in `templates/`
- [Bootstrap](http://getbootstrap.com/), a CSS / JS template that gives your page a solidly 
  presentable (albeit not terribly creative) layout.
- Create Heroku application with `heroku create <app_name>` or leave blank to
  auto-generate a name.
- (Suggested) Use the [conda buildpack](https://github.com/kennethreitz/conda-buildpack).
  `heroku config:add BUILDPACK_URL=https://github.com/kennethreitz/conda-buildpack.git`
  If you choose not to, put all requirements into `requirements.txt`
- Deploy to Heroku: `git push heroku master`
- You should be able to see your site at `https://<app_name>.herokuapp.com`
- A useful reference is the Heroku [quickstart guide](https://devcenter.heroku.com/articles/getting-started-with-python-o).

## Step 2: Get data from API and put it in pandas
- Use the `requests` library to grab some data from a public API. This will
  often be in JSON format, in which case `simplejson` will be useful.
- Build in some interactivity by having the user submit a form which determines which data is requested.
- Create a `pandas` dataframe with the data.

## Step 3: Use Bokeh to plot pandas data
- Create a Bokeh plot from the dataframe.
- Consult the Bokeh [documentation](http://bokeh.pydata.org/en/latest/docs/user_guide/embed.html)
  and [examples](https://github.com/bokeh/bokeh/tree/master/examples/embed).
- Make the plot visible on your website through embedded HTML or other methods - this is where Flask comes in to manage the interactivity and display the desired content.
- Some good references for Flask: [This article](https://realpython.com/blog/python/python-web-applications-with-flask-part-i/), especially the links in "Starting off", and [this tutorial](https://github.com/bev-a-tron/MyFlaskTutorial).
