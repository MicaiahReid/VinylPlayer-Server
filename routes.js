"use strict";

const auth = require("./lib/routes/auth");
const discogs = require("./lib/routes/discogs");
const catalog = require("./lib/routes/catalog");
const spawn = require("child_process").spawn;
const fs = require("fs");

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

	app.post("/searchImage", (req, res) => {
		let encodedImage = req.body.image;
		// encodedImage = encodedImage.substring(2, encodedImage.length - 5);
		// let delimitedEncodeImage = encodedImage.split(" ");
		// encodedImage = delimitedEncodeImage.join("");

		let decodedImage = new Buffer(encodedImage, 'base64');

		fs.writeFile("./lib/bin/img/original.JPG", decodedImage, function(err) {
			if(err) { 
				console.log(err); 
			}
		
			console.log("The file was saved!");
		});

		const process = spawn("python", ["./lib/bin/ocr.py", "./lib/bin/img/original.JPG"]);
		process.stdout.on("data", (data) => {
			console.log(data)
			// data = JSON.parse(String.fromCharCode.apply(null, data));
			// console.log(data.data);
			res.send("worddddd")
			


			// req.body.artist = data.artist;
			// req.body.album = data.album;
			// discogs.searchDiscogs(req, res);
		});

		process.stdout.on('data', (data) => {
			console.log(`stdout: ${data}`);
		});
		  
		process.stderr.on('data', (data) => {
			console.log(`stderr: ${data}`);
		});
		
		process.on('close', (code) => {
			console.log(`child process exited with code ${code}`);
		});
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
		isAuthenticated(req, (error, exists) => {
			if(error) {
				res.status(500).send(error);
			}
			else if(exists) {
				res.status(202).send("already logged in");
			}
			else {
				auth.authenticateUser(req, res);
			}
		});
	});

	app.post("/logout", (req, res) => {
		isAuthenticated(req, (error, exists) => {
			if(error) {
				res.status(500).send(error);
			}
			else if(!exists) {
				res.status(202).send("not logged in");
			}
			else {
				auth.deleteSession(req, res);
			}
		});
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

	app.post("/jobNimbusTest", (req, res) => {
		console.log(req);
	});
};