"use strict";

const pool = require("./lib/db");

module.exports = (app) => {

	app.post("/records/:id", (req, res) => {
		const recordId = req.params.id;
		res.send(recordId);
	});

	app.post("/records/search/:name", (req, res) => {
		const recordName = req.params.name;
		pool.query("SELECT id, artist_id, name FROM records WHERE name LIKE $1", [recordName], (error, results) => {
			if(error) {
				console.log(error.message);
				res.send(error);
			}
			else {
				res.send(results.rows);
			}
		})
	});
}