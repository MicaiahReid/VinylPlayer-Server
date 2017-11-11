"use strict";

module.exports = (app) => {

	app.post("/records/:id", (req, res) => {
		const recordId = req.params.id;
		res.send(recordId);
	});

	app.post("/records/search/:name", (req, res) => {
		res.send(req.params.name);
	});
}