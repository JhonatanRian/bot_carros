"use strict";

const browserInstance = require("./browser");
const scrapers = require("./bot");

const puppeteer = require('puppeteer');


async function main() {
    let objs
    let browser

    while (true){
        try{
            browser = await browserInstance()
            objs = await scrapers.scraper(browser)
            await browser.close()
            break
        }catch{
            console.log("ERROR SCRAPER, TENTANDO NOVAMENTE")
            await browser.close()

        }
    }
    


    for (let i = 0 ; i < objs.length ; i++){
        while (true){
            try{
                browser = await browserInstance()
                let own = await scrapers.get_info(browser, objs[i].source)
                objs[i].owner = own
                browser.close()
                break
            }catch{
                console.log("ERROR SCRAPER, TENTANDO NOVAMENTE")
                await browser.close()
            }
        }

    }

    await scrapers.save(objs)


}

main();