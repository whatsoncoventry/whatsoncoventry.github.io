const Database = require('sqlite-async')
const dbName = 'woCoventry.db'


exports.subscribe = async (query, name, email) =>{

    if(query !== undefined && name !== undefined && email !== undefined) {
        const sql = `INSERT INTO newsletter VALUES ("${email}", "${name}");`
        console.log(sql)
        const db = await Database.open(dbName)
        await db.run(sql)
        await db.close()
        message = 'Thank you for subscribing'
    exports.message = message
    }
}
