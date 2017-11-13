"use strict";

const pool = require("./lib/db");
const auth = require("./lib/routes/auth");

module.exports = (app) => {
	app.post("/records/:id", (req, res) => {
		const recordId = req.params.id;
		res.send(recordId);
	});

	app.post("/records/search/:name", (req, res) => {
		console.log("Made it to route /records/search/:name");
		const recordName = req.params.name;
		console.log("Record name sent was: " + recordName);
		pool.query("SELECT id, artist_id, name FROM records WHERE name LIKE $1", [recordName], (error, results) => {
			if(error) {
				console.log(error.message);
				res.send(error);
			}
			else {
				console.log("Results found: " + JSON.stringify(results.rows));
				res.send(results.rows);
			}
		});
	});

	app.post("/login", (req, res) => {
		auth.authenticateUser(req, res, (valid) => {
			if(!valid) {
				res.send("Invalid Credentials");
			}
			else {
				res.send("User Authenticated");
			}
		});
	});

	app.post("/createUser", (req, res) => {
		auth.createUser(req, res);
	});
};