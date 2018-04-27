"use strict";
var discogs = require("disconnect").Client;
var discogsDB = discogs("VinylPlayerApp/1.0", {"userToken": process.env.DISCOGS_API_TOKEN}).database();
const async = require("async");

module.exports.queryDiscogs = (req, res) => {
	const query = req.body.query;
	const params = { 
		"type": "master",
		"per_page": 100
	}
	
	// perform Discogs query
	// if error then return error
	// else sort and filter results
	discogsDB.search(query, params, (error, response) => {
		if(error) { res.send(error); }
		
		const results = response.results;
		let filteredResults = [];
		let artists = [];
		res.send(results); 
	});
}

module.exports.getTracklist = (req, res) => {
	var id = req.body.id;
	var hasDurations = true;
	var tracklist = []

	discogsDB.getMaster(id, (error, master) => {
		if(error) {
			res.send(error);
		}

		else {
			// check if record has durations for every song
			// if not then don't add to the results
			const masterTracklist = master.tracklist;
			for(var i=0; i<masterTracklist.length; i++) {
				let track = masterTracklist[i];
				if(track.duration === "") {
					hasDurations = false;
					break;
				}
			}

			if(hasDurations) {	
				tracklist = masterTracklist;		
				discogsDB.getMasterVersions(id, (error, versions) => {	
					if(error) {
						res.send(error);
					}

					let masterVersions = versions.versions;
					let j = 0;
					async.whilst(() => { return j < masterVersions.length; }, 
						(callback) => {
							let masterVersion = masterVersions[j++];
							if(masterVersion.major_formats.indexOf("Vinyl") == -1) { callback(); }
							else {
								var releaseId = masterVersion.id;
								discogsDB.getRelease(releaseId, (error, release) => {							
									
									let hasPositions = true;
									const releaseTracklist = release.tracklist;
									let k = 0;
									async.whilst(() => { return k < releaseTracklist.length; }, 
										(callback) => {
											let track = releaseTracklist[k];
											tracklist[k].position = track.position;
											k++
											callback();
										}, (error) => { 
											res.send(tracklist); 
										}
									);
								});
							 	callback();
							}
						}, (error) => {}
					);
				});
			}
			else { res.send(error); }
		}
	});
}

// module.exports.searchDiscogs = (req, res) => {
// 	const artist = req.body.artist;
// 	const album = req.body.album;
// 	const filter = {
// 		"artist": artist,
// 		"release_title": album,
// 		// "track": searchText,
// 		"format": "Vinyl",
// 		"searchType": "master",
// 		"per_page": 100
// 	};
// 	discogsDB.search(filter, (error, results) => {
// 		if(error) {
// 			res.send(error);
// 		}
// 		else {
// 			const allResults = results.results;
// 			var resultsByArtist = [];
// 			var artists = [];
// 			const processRecords = (id, album, titleParts, artist, cover, year, albumId, callback) => {
// 				discogsDB.getRelease(id, (error, results) => {
// 					if(error) {
// 						if(error.message == "Release not found.") {
// 							callback();
// 						}
// 						if(error.message == "The requested resource was not found."){
// 							callback();
// 						}
// 						else {
// 							throw error;
// 						}
// 					}
// 					else {
// 						let hasDurations = true;
// 						const tracklist = results.tracklist;
// 						tracklist.forEach((track) => {
// 							if(track.duration === "") {
// 								hasDurations = false;
// 							}
// 						});
// 						if(hasDurations) {
// 							artists.push(artist);
// 							resultsByArtist.push({
// 								"artist": artist,
// 								"album": titleParts[1],
// 								"id": album.id,
// 								"thumbnail": album.thumb,
// 								"tracklist": tracklist,
// 								"url": cover,
// 								"year": year,
// 								"albumId": albumId
// 							});
// 						}
// 						callback();
// 					}
// 				});
// 			};

// 			let i = 0;
// 			const l = 10;
// 			if(l > 0) {
// 				async.whilst( () => {return i < l;}, (callback) => {
// 						const result = allResults[i];
// 						if(result == null) { callback(); }
// 						const titleParts = result.title.split(" - ");
// 						const artist = titleParts[0];
// 						const album = titleParts[1];
// 						const tracklist = result.tracklist;
// 						const cover = result.thumb;
// 						const year = result.year;
// 						const albumId = result.id;

// 						i++;
// 						if(!artists.includes(artist)) {
// 							processRecords(parseInt(result.id), album, titleParts, artist, cover, year, albumId, callback);
// 						}
// 						else {
// 							callback();
// 						}
// 					},
// 					() => {
// 						res.send(resultsByArtist);
// 					}
// 				);
// 			}
// 			else {
// 				res.sendStatus(404);
// 			}
// 		}
// 	});
// };

