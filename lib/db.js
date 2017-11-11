"use strict";

const Pool = require("pg").Pool;
const pool = new Pool({
	"user": process.env.DATABASE_USER,
	"password": process.env.DATABASE_PASSWORD,
	"host": process.env.DATABASE_HOST,
	"database": process.env.DATABASE_DATABASE,
	"max": 10
});
pool.on("error", (error, client) =>{
	console.log(error);
});

// export the query method for passing queries to the pool
module.exports.query = (text, values, callback) => {
	return pool.query(text, values, callback);
};