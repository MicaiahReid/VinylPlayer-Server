"use strict";

const discogs = require("disconnect").Client;
const discogsDB = discogs("VinylPlayerApp/1.0", {"userToken": process.env.DISCOGS_API_TOKEN}).database();
const async = require("async");

module.exports.searchDiscogs = (req, res) => {
	const artist = req.body.artist;
	const album = req.body.album;
	const filter = {
		"artist": artist,
		"release_title": album,
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
			const allResults = results.results;
			let resultsByArtist = [];
			let artists = [];
			const processRecords = (id, album, titleParts, artist, callback) => {
				discogsDB.getRelease(id, (error, results) => {
					if(error) {
						if(error.message === "Release not found.") {
							callback();
						}
						else {
							throw error;
						}
					}
					else {
						let hasDurations = true;
						const tracklist = results.tracklist;
						tracklist.forEach((track) => {
							if(track.duration === "") {
								hasDurations = false;
							}
						});
						if(hasDurations) {
							artists.push(artist);
							resultsByArtist.push({
								"artist": artist,
								"year": album.year,
								"album": titleParts[1],
								"id": album.id,
								"thumbnail": album.thumb
							});
						}
						callback();
					}
				});
			};

			let i = 0;
			const l = allResults.length;
			if(l > 0) {
				async.whilst(
					() => {return i < l;},
					(callback) => {
						const album = allResults[i];
						const titleParts = album.title.split(" - ");
						const artist = titleParts[0];
						i++;
						if(!artists.includes(artist)) {
							processRecords(parseInt(album.id), album, titleParts, artist, callback);
						}
						else {
							callback();
						}
					},
					() => {
						res.send(resultsByArtist);
					}
				);
			}
			else {
				res.sendStatus(404);
			}
		}
	});
};

module.exports.getAlbumInfo = (req, res, callback) => {
	const data = req.body;
	const id = parseInt(data.id);

	discogsDB.getRelease(id, (error, results) => {
		if(error) {
			callback(error);
		}
		else {
			const artist = results.artists[0]; // we'll only use the 1st listed artist's information
			const album = {
				"id": results.id,
				"artistId": artist.id,
				"artistName": artist.name,
				"thumbnail": results.thumb,
				"album": results.title,
				"tracklist": results.tracklist
			};
			callback(null, album);
		}
	});
};