# Setup

```
npm install create-react-app
npx create-react-app frontend
```

## Check to make sure it's installed correctly
```
cd frontend
npm start
```

## install rest of react
`npm install axios react-bootstrap bootstrap font-awesome --save`

### Add this to settings.py
```
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
```
### Add this to package.json
`"proxy": "http://127.0.0.1:8000",`

### Add this to public/index.html header tag
```angular2html
<link rel=”stylesheet” 
      href=”https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" 
      integrity=”sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T” 
      crossorigin=”anonymous”/>
```