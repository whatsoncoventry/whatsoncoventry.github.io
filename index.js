#!/usr/bin/env node

'use strict'
    const Koa = require('koa')
    const Router = require('koa-router')
    const stat = require('koa-static')
    const Database = require('sqlite-async')
    const handlebars = require('koa-hbs-renderer')
    const cmd = require('node-cmd')
    const schedule = require('node-schedule')
    const newsletter = require('./assets/js/newsletter.js')
    const events = require('./assets/js/events.js')
    
const app = new Koa()
const router = new Router()
app.use(handlebars({ paths: { views: `${__dirname}/views` } }))
app.use(stat('assets'))
app.use(router.routes())

const PORT = process.env.PORT || 3000;
const dbName = 'woCoventry.db'

router.get('/', async ctx => {
	try {
        	await newsletter.subscribe(ctx.query, ctx.query.name, ctx.query.email)
		
        	await ctx.render('index')
     } 	catch(err) {
		ctx.body = err.message
	}
})

router.get('/events', async ctx => {
	try {
        	let results = await events.events(ctx.query, ctx.query.q)
        
        	await newsletter.subscribe(ctx.query, ctx.query.name, ctx.query.email) 
        
        	await ctx.render('events', {events: results.data, query: results.querystring})
      } catch(err) {
		ctx.body = err.message
	}
})

router.get('/visit', async ctx => {
	try {
		await newsletter.subscribe(ctx.query, ctx.query.name, ctx.query.email) 
		
        	await ctx.render('visit')
        } catch(err) {
		ctx.body = err.message
	}
})

router.get('/news', async ctx => {
	try {
		await newsletter.subscribe(ctx.query, ctx.query.name, ctx.query.email) 
        
		await ctx.render('news')
        } catch(err) {
		ctx.body = err.message
	}
})

router.get('/discovery', async ctx => {
	try {
		await newsletter.subscribe(ctx.query, ctx.query.name, ctx.query.email) 
        
		await ctx.render('discovery')
        } catch(err) {
		ctx.body = err.message
	}
})

router.get('/media', async ctx => {
	try {
		await newsletter.subscribe(ctx.query, ctx.query.name, ctx.query.email) 
        
		await ctx.render('media')
        } catch(err) {
		ctx.body = err.message
	}
})

var connection = app.listen(PORT, () => console.log(`listening on port ${ PORT }`))


const scraper = schedule.scheduleJob({second: 5}, function(){
    connection.close(console.log.bind(console, "Server got restarted for update."))
    cmd.run('python3 views/scrapescript.py')
    console.log("built")
    connection = app.listen(PORT, () => console.log(`listening on port ${ PORT }`))
})
