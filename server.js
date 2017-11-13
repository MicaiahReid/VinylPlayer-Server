"use strict";

const express = require("express");
const bodyParser = require("body-parser");
const app = express();

const routes = require("./routes");

app.use(bodyParser.urlencoded());
app.use(bodyParser.json());

routes(app);

// catch all paths that weren't found in routes
app.get("*", (req, res) => {
	res.status(404).send("404");
});

app.all("*", (req, res) => {
	res.status(404);
});

app.listen(process.env.PORT || 3001, () => {
	console.log("App started and listening on port " + (process.env.PORT || 3001));
});