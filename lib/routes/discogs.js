"use strict";

const discogs = require("disconnect").Client;
const discogsDB = discogs("VinylPlayerApp/1.0", {"userToken": process.env.DISCOGS_API_TOKEN}).database();

module.exports.searchDiscogs = (req, res) => {
	const searchText = req.body.searchText;
	const filter = {
		"artist": searchText,
		// "title": searchText,
		// "track": searchText,
		"format": "Vinyl",
		"searchType": "all",
		"per_page": 100
	};
	discogsDB.search(filter, (error, results) => {
		if(error) {
			res.send(error);
		}
		else {
			res.send(results);
		}
	});
};
