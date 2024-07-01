# Temperature manager


## 👩‍💻 _Installation & Run_

### 📝 Set enviroment variable
- Copy and rename the **.env.sample** file to **.env** 
- Open the .env file and edit the environment variables 
- Save the .env file securely 
- Make sure the .env file is in .gitignore

 On Windows:
```python
python -m venv venv 
venv\Scripts\activate
 ```

 On UNIX or macOS:
```python
python3 -m venv venv 
source venv/bin/activate
 ```

### 🗃️ Install requirements 
```python
pip install -r requirements.txt
```


### 🗃️ Start project
```python
python uvicorn main:app --reload
```

### 😄 Go to site [http://localhost:8000/](http://localhost:8000/)


## 😋 _Enjoy it!_