"use strict";

const browserInstance = require("./browser");
const scrapers = require("./bot");

const puppeteer = require('puppeteer');


async function main() {
    let browser = await browserInstance()

    await scrapers.scraper(browser)
    
    browser.close()
}

main();