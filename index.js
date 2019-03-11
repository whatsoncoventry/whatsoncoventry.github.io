#!/usr/bin/env node

'use strict'
    const Koa = require('koa')
    const Router = require('koa-router')
    const stat = require('koa-static')
    const Database = require('sqlite-async')
    const handlebars = require('koa-hbs-renderer')
    

const app = new Koa()
const router = new Router()
app.use(handlebars({ paths: { views: `${__dirname}/views` } }))
app.use(stat('assets'))
app.use(router.routes())

const PORT = process.env.PORT || 3000;
const dbName = 'woCoventry.db'

router.get('/', async ctx => {
	try {
        let newslettermessage = 'Sign up to our newsletter'
        if(ctx.query !== undefined && ctx.query.newsletter !== undefined) {
            const sql = `INSERT INTO newsletter VALUES ("${ctx.query.newsletter}");`
            newslettermessage = 'Thank you for subscribing'
            const db = await Database.open(dbName)
            await db.run(sql)
            await db.close()
        }        
        await ctx.render('index', {message: newslettermessage})
    } catch(err) {
		ctx.body = err.message
	}
})

router.get('/events', async ctx => {
	try {
        let sql = 'SELECT eventname, eventdescription, eventdate, eventtime, eventpostcode, eventaddress, eventimage FROM eventspage;'
		let querystring = ''
		console.log(ctx.query.q)
		if(ctx.query !== undefined && ctx.query.q !== undefined) {
			sql = `SELECT eventname, eventdescription, eventdate, eventtime, eventpostcode, eventaddress, eventimage FROM eventspage 
							WHERE  upper(eventname) LIKE upper("%${ctx.query.q}%");`
			querystring = ctx.query.q
		}
		const db = await Database.open(dbName)
		const data = await db.all(sql)
		await db.close()
		console.log(data)
        await ctx.render('events', {events: data, query: querystring})
        } catch(err) {
		ctx.body = err.message
	}
})

router.get('/visit', async ctx => {
	try {
        await ctx.render('visit')
        } catch(err) {
		ctx.body = err.message
	}
})

router.get('/news', async ctx => {
	try {
        await ctx.render('news')
        } catch(err) {
		ctx.body = err.message
	}
})

module.exports = app.listen(PORT, () => console.log(`listening on port ${ PORT }`))
