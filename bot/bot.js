"use strict";
const { default: axios } = require('axios');
const fs = require('fs');

const SOURCE_NAME = "webmotors";
const objScraper = {
    name: SOURCE_NAME,
    URL: "https://www.webmotors.com.br/carros/estoque?tipoveiculo=carros&anunciante=Pessoa%20F%C3%ADsica",
    async scraper(browser) {
        const page = await browser.newPage();
        await page.setViewport({ width: 1010, height: 730 });
        while (true){
            try{
                console.log(`scrapper ${this.URL}`);
                await page.goto(this.URL, {timeout: 5000000});
                await page.waitForSelector('.sc-gqPbQI')
                break
            }catch{
                console.log("falha na requisição. Tentanto novamente")
            }
        }
        
        let carDivs = await page.$$(".sc-gqPbQI")
        const lista = []
        console.log("Analizando a pagina.")
        await carDivs.forEach(async(element, index) => {
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
                return Array.from([img,link,name,price, km, ano])
            }, index)
            lista.push(res)
        });
        console.log("analise finalizada")

        await page.close()

        return await this.generateObjs(lista)
    },

    async generateObjs(arr){
        let lto = new Array
        await arr.forEach(async result => {

            lto.push({
                img: result[0],
                source: result[1],
                name: result[2],
                price: result[3],
                km: result[4],
                year: result[5]
            })
            
        });
        return lto
    },

    async get_info(browser, url){
        const page = await browser.newPage();
        await page.setViewport({ width: 1010, height: 730 });
        while (true){
            try{
                console.log(`scrapper ${url}`);
                await page.goto(url, {timeout: 5000000});
                await page.waitForSelector('#VehicleCharacteristic > div > ul')
                break
            }catch{
                console.log("falha na requisição. Tentanto novamente")
            }
        }
        
        let res = await page.evaluate(async () => {
            let text = document.querySelector("#VehicleCharacteristic > div > ul").textContent
            if(text.includes("Único donoSim")){
                return "1"
            }else{
                return "2"
            }
        })
        await page.waitForTimeout(5000)
        await page.close()
        return res
    },

    async save(data){
        axios.post("http://127.0.0.1:8000/", JSON.stringify(data), {headers: {'Content-Type': 'application/json'}})
            .then((resolve) => {
                console.log(resolve)
            })
            .catch((err) => {
                console.log(err)
            })
    }
};

module.exports = objScraper;