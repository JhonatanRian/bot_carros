const puppeteer = require('puppeteer-extra');
// const AdblockerPlugin = require('puppeteer-extra-plugin-adblocker')
    // const fullPageScreenshot = require('puppeteer-full-page-screenshot')


async function start() {
    let browser;

    try {
        console.log("Abrindo navegador......");
        // puppeteer.use(AdblockerPlugin())
        browser = await puppeteer.launch({
            headless: true,
            devtools: true,
            // executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            args: [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-web-security",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-features=IsolateOrigins,site-per-process",
            ],
            ignoreHTTPSErrors: true,
        });

    } catch (error) {
        console.log(error)
    }
    return browser;
}

module.exports = start