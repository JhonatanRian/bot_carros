"use strict";

const browserInstance = require("./browser");
const scrapers = require("./bot");

const puppeteer = require('puppeteer');


async function main() {
    let browser = await browserInstance()

    let objs = await scrapers.scraper(browser)
    
    await browser.close()


    for (let i = 0 ; i < objs.length ; i++){
        browser = await browserInstance()
        let own = await scrapers.get_info(browser, objs[i].source)
        objs[i].owner = own
        browser.close()

    }

    await scrapers.save(objs)


}

main();