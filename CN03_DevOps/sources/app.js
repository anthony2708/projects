const express = require('express');
const path = require('path');
const app = express();

// Router here
const homeRouter = require('./routes/homeRoute');

// Some checking
app.use(express.json());
app.use(express.urlencoded({
    extended: true
}));

app.set('view engine', 'ejs');
app.use('/', homeRouter);

app.use(express.static(path.join(__dirname + '/public')));
app.all('*', (req, res, next) => {
    next(console.log(`Can't find ${req.originalUrl} on this server`, 404));
});

module.exports = app;