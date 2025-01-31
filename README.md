
# StockSage

Your personal AI-powered stock prediction tool, designed to make stock analysis easier and more accessible. Whether you're an investor looking to predict stock trends or just a data enthusiast, Stocksage has got you covered.

- **Train Your Custom Model**: Tailor a prediction model to match your unique strategies. Train it with the data that matters most to you.

- **Predict the Stocks You Want**: Use advanced AI to forecast stock prices and trends, helping you stay ahead of the curve.

- **Track Your Portfolio**: Keep an eye on your investments and watch your portfolio grow with real-time tracking.

- **AI Integration**: Harness the power of AI to give you insights that go beyond traditional analysis.

- **User-Friendly GUI**: No complicated setups or confusing interfaces. Stocksage is designed to be intuitive and easy to navigate for anyone.

Sounds Fun? Check it out [here]()!

---
\
With the sales pitch out of the way, this is my first ***actual*** project that I want to ***complete***.

It is a full stack app using [__Django__](https://www.djangoproject.com/) for its backend and [__SvelteKit__](https://svelte.dev/) for its frontend. The details of the respective projects can be found _in their own_ 'README.md files'

<hr>

# Quick SetUp

Basic Steps:
```
git clone 'https://github.com/lucifer1147/stocksage.git'
cd stocksage
```

To install all the dependencies:

```
cd stocksage_backend
python -m venv .venv
.venv\scripts\activate
pip install -r requirements.txt

cd ..
cd stocksage_frontend
npm install

```

To use the CLI (use `python main.py [command] -h` to see the various options):

```
cd stocksage_backend
.venv\scripts\activate
python main.py [command] [options...]
```

To host the backend locally:
```
cd stocksage_backend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

To host the frontend locally (use the latter if you wish to preview the production build):
```
cd stocksage_frontend
npm run dev
```
***OR***
```
cd stocksage_frontend
npm run build
npm run preview
```