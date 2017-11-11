"use strict";

const express = require("express");
const app = express();

const routes = require("./routes");

routes(app);

// catch all paths that weren't found in routes
app.post("*", (req, res) => {
	res.status(404);
});

app.listen(3001);