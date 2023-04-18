# Sports statistics measurement system

### Installation
Install dependencies from the repository directory:
1. **frontend**
```bash
$ npm install
```
2. **backend**
```bash
$ pip install -r requirements.txt
```

### Setup (development)
**To start everything together**:
```bash
$ npm start
```
**To run everything separately**:
1. Start frontend:
```bash
$ npm parcel
```
2. Start backend:
```bash
$ flask --app server run
```

You can access the website on `http://localhost:1234`.

### Bulding (production)
```bash
$ npm build
```

### Known bugs:
* `sqlite3.OperationalError: no such column: undefined` when clicking on one of the seasons
* Adding new match doesn't refresh the matches on main page (old cached version is shown instead)
* Entire AppBar can be clicked instead of just the title of the page (because of the `flexGrow` attribute)

### DO NOT UPLOAD `node_modules` NOR `dist` FOLDER NOR `.parcel-cache` NOR `__pycache__`!
