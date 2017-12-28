"use strict";

const auth = require("./lib/routes/auth");
const discogs = require("./lib/routes/discogs");
const catalog = require("./lib/routes/catalog");

const isAuthenticated = (req, callback) => {
	const userId = req.cookies["_vinylPlayer_userId"];
	const sessionId = req.cookies["_vinylPlayer_sessionId"];
	if(typeof sessionId !== "undefined" && sessionId !== "" && typeof userId !== "undefined" && userId !== "") {
		auth.isAuthenticated(sessionId, userId, (error, exists) => {
			callback(error, exists);
		});
	}
	else {
		callback(null, false);
	}
};

const continueIfAuthenticated = (req, res, next) => {
	isAuthenticated(req, (error, authenticated) => {
		if(error) {
			res.status(400).send("not logged in");
		}
		else if(authenticated) {
			next();
		}
		else {
			res.status(400).send("not logged in");
		}
	});
};

module.exports = (app) => {
	app.post("/records/:id", continueIfAuthenticated, (req, res) => {
		const recordId = req.params.id;
		res.send(recordId);
	});

	app.post("/search", continueIfAuthenticated, (req, res) => {
		discogs.searchDiscogs(req, res);
	});

	app.post("/getAlbumInfo", continueIfAuthenticated, (req, res) => {
		discogs.getAlbumInfo(req, res, (error, album) => {
			if(error) {
				res.status(500).send(error);
			}
			else {
				res.send(album);
			}
		});
	});
	app.post("/search/:id", continueIfAuthenticated, (req, res) => {

	});
	app.post("/login", (req, res) => {
		auth.authenticateUser(req, res);
	});

	app.post("/createUser", (req, res) => {
		auth.createUser(req, res);
	});

	app.post("/catalog", continueIfAuthenticated, (req, res) => {
		catalog.getCatalog(req, res);
	});

	app.post("/addAlbum", continueIfAuthenticated, (req, res) => {
		catalog.addAlbum(req, res);
	});
};