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

const port = 8080
const dbName = 'woCoventry.db'

router.get('/', async ctx => {
	try {
        
        await ctx.render('index')
    } catch(err) {
		ctx.body = err.message
	}
})

router.get('/events', async ctx => {
	try {
        let sql = 'SELECT eventname, eventdescription, eventdate, eventtime, eventpostcode, eventaddress FROM eventspage;'
		let querystring = ''
		console.log(ctx.query.q)
		if(ctx.query !== undefined && ctx.query.q !== undefined) {
			sql = `SELECT eventname, eventdescription, eventdate, eventtime, eventpostcode, eventaddress FROM eventspage 
							WHERE  upper(eventname) LIKE upper("%${ctx.query.q}%");`
			querystring = ctx.query.q
		}
		const db = await Database.open(dbName)
		const data = await db.all(sql)
		await db.close()
		console.log(data)
        await ctx.render('search', {events: data, query: querystring})
        } catch(err) {
		ctx.body = err.message
	}
})

router.get('/elements', async ctx => {
	try {
        await ctx.render('elements')
        } catch(err) {
		ctx.body = err.message
	}
})

router.get('/generic', async ctx => {
	try {
        await ctx.render('generic')
        } catch(err) {
		ctx.body = err.message
	}
})

module.exports = app.listen(port, () => console.log(`listening on port ${port}`))