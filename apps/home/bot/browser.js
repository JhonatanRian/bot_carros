const puppeteer = require('puppeteer-extra');


async function start() {
    let browser;

    console.log("Abrindo navegador......");
    // puppeteer.use(AdblockerPlugin())
    browser = await puppeteer.launch({
        headless: false,
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
    return browser;
}

module.exports = start