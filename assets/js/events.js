const Database = require('sqlite-async')
const dbName = 'woCoventry.db'

exports.events = async (query, q) =>{
    let sql = 'SELECT eventname, eventdescription, eventdate, eventtime, eventpostcode, eventaddress, eventimage FROM eventspage;'
		let querystring = ''
		console.log(q)
		if(query !== undefined && q !== undefined) {
			sql = `SELECT eventname, eventdescription, eventdate, eventtime, eventpostcode, eventaddress, eventimage FROM eventspage 
							WHERE  upper(eventname) LIKE upper("%${q}%")
                            OR upper(eventpostcode) LIKE upper("%${q}%")
                            OR upper(eventaddress) LIKE upper("%${q}%");`
			querystring = q
		}
		const db = await Database.open(dbName)
		const data = await db.all(sql)
		await db.close()
		console.log(data)
    return { data, querystring }
}
