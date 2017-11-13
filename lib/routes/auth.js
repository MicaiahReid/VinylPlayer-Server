"use strict";

const easyPbkdf2 = require("easy-pbkdf2")({
	"DEFAULT_HASH_ITERATIONS": 20000,
	"SALT_SIZE": 180,
	"KEY_LENGTH": 250
});
const pool = require("../db");
const async = require("async");

module.exports.authenticateUser = (req, res, callback) => {
	const email = req.body.email;
	const password = req.body.password;

	pool.query("SELECT id, email, password, salt FROM users WHERE email = $1", [email], (error, result) => {
		if(error) {
			res.send(error);
		}
		else {
			let user = result.rows[0];
			if(!user) {
				// user not found
				res.status(404);
			}
			else {
				easyPbkdf2.verify(user.salt, user.password, password, (err, valid) => {
					if(err) {
						throw err;
					}
					else {
						callback(valid);
					}
				});
			}
		}
	});
};

module.exports.createUser = (req, res) => {
	const email = req.body.email;
	const password = req.body.password;

	async.series({
		"checkUser": (callback) => {
			pool.query("SELECT id FROM users WHERE email = $1", [email], (error, result) => {
				if(error) {
					throw error;
				}
				callback(null, result.rows);
			});
		}
	}, (error, result) => {
		if(error) {
			res.send(error);
		}
		else {
			const userExists = result.checkUser.length > 0;
			if(userExists) {
				res.send("User already exists");
			}
			else {
				const salt = easyPbkdf2.generateSalt();
				easyPbkdf2.secureHash(password, salt, (error, hash) => {
					if(error) {
						throw error;
					}
					pool.query(
						`WITH insertUser AS (
							INSERT INTO users (email, password, salt) VALUES ($1, $2, $3) RETURNING id
						),
						insertSession AS (
							INSERT INTO sessions (user_id, expires_at) VALUES ((SELECT id FROM insertUser), CURRENT_TIMESTAMP + INTERVAL '30' day) RETURNING id, user_id
						)
						SELECT id, user_id FROM insertSession`, [email, hash, salt], (error, result) => {
							if(error) {
								res.send(error);
							}
							else {
								const sessionId = result.rows[0].id;
								const userId = result.rows[0].user_id;

								res.cookie("_vinylPlayer_sessionId", sessionId, {"httpOnly": true});
								res.cookie("_vinylPlayer_userId", userId, {"httpOnly": true});
								res.send("User Created and Authenticated");
							}
						}
					);
				});
			}
		}
	});
};