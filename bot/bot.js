"use strict";
const fs = require('fs');

const SOURCE_NAME = "webmotors";
const objScraper = {
    name: SOURCE_NAME,
    URL: "https://www.webmotors.com.br/carros/estoque?idcmpint=t1:c17:m07:webmotors:busca::verofertas",
    async scraper(browser) {
        console.log(`scrapper ${this.URL}`);
        const self = this;
        const page = await browser.newPage();
        await page.setViewport({ width: 1010, height: 730 });
        await page.goto(self.URL, {timeout: 5000000});
        await page.waitForSelector('.sc-gqPbQI')
        let carDivs = await page.$$(".sc-gqPbQI")
        const lista = []
        console.log("Analizando a pagina.")
        carDivs.forEach((element, index) => {
            lista.push(this.capture(page, index))
        });
        await page.waitForTimeout(5000)
        console.log("Processando analisa e salvando os dados")
        await this.saving(lista)
        page.close()
        page.close()
    },

    async capture(page, i){
        let index = i
        let res = await page.evaluate((index)=>{
            let elements = document.querySelectorAll(".sc-gqPbQI")
            let element = elements[index]
            let img
            try{
                img = element.querySelector("img").attributes.src.value
            }catch{
                img = "/static/assets/images/497833.png"
            }
            let link = element.querySelector("div div:nth-child(2) a").attributes.href.value
            let name = element.querySelector("div div:nth-child(2) a div").textContent
            let price = element.querySelector("div div:nth-child(2) a:nth-child(2) div strong").textContent
            let km = element.querySelector("div div:nth-child(2) a:nth-child(2) div:nth-child(2) div:nth-child(2)").textContent
            let ano = element.querySelector("div div:nth-child(2) a:nth-child(2) div:nth-child(2) div:nth-child(1)").textContent
            return Array.from([`${img}`,`${link}`,`${name}`,`${price}`, `${km}`, `${ano}`])
        }, index)
        return res
    },

    async saving(arr){
        let lto = new Array
        await arr.forEach(element => {
            element.then((result) => {
                lto.push({
                    img: result[0],
                    source: result[1],
                    name: result[2],
                    price: result[3],
                    km: result[4],
                    year: result[5]
                })
            }).catch((err) => {
                console.log(err)
            });
        });
        await this.saveJson(lto)
    },

    async saveJson(data){
        fs.writeFile(__dirname + "car.json", JSON.stringify(data), function(err) {
            if(err) {
                console.log(err);
            } else {
                console.log("The file was saved!");
            }
        });
    }
};

module.exports = objScraper;