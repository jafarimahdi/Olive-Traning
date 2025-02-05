-   <a href="#skyscanner" id="toc-skyscanner">Skyscanner</a>
-   <a href="#mnb" id="toc-mnb">MNB</a>

# Skyscanner

``` r
library(jsonlite)
library(data.table)
```

``` r
# places
ll <- fromJSON('https://partners.api.skyscanner.net/apiservices/reference/v1.0/locales?apiKey=apikey')
fromJSON('https://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/HU/HUF/en-US?query=hungary&apiKey=apikey')
```

``` r
from<-"2022-12-08"
to<-"2022-12-14"
url<-paste0("https://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/HU/HUF/en-US/BUD-sky/Anywhere/",from,"/",to,"?apiKey=",readLines('/home/mihaly/R_codes/ECBS-5306-Coding-2-Web-Scraping-with-R/week-5/apikey'))
t <- fromJSON(url, flatten = T)
```

``` r
flights <- data.table(t$Quotes)
places<- data.table(t$Places)
carrier<- data.table(t$Carriers)
flights$OutboundLeg.CarrierIds <- unlist(flights$OutboundLeg.CarrierIds)
flights$InboundLeg.CarrierIds <- unlist(flights$InboundLeg.CarrierIds)
places<-places[complete.cases(places),]
get_city<-function(places_df,myid){
  return(places_df[PlaceId==myid,]$CityName)
}
get_country<-function(places_df,myid){
  return(places_df[PlaceId==myid,]$CountryName)
}
get_carrier<-function(carrier_df,myid){
  return(carrier_df[CarrierId==myid,]$Name)
}
get_carrier(carrier, flights$OutboundLeg.CarrierIds[1])
```

``` r
for(i in c(1:nrow(flights))){
  flights$Country[i]<-get_country(places,flights$OutboundLeg.DestinationId[i])
  flights$OutboundLeg.OriginId[i]<-get_city(places,flights$OutboundLeg.OriginId[i])
  flights$InboundLeg.OriginId[i]<-get_city(places,flights$InboundLeg.OriginId[i])
  
  flights$OutboundLeg.DestinationId[i]<-get_city(places,flights$OutboundLeg.DestinationId[i])
  flights$InboundLeg.DestinationId[i]<-get_city(places,flights$InboundLeg.DestinationId[i])
  
  flights$OutboundLeg.CarrierIds[i]<-get_carrier(carrier,flights$OutboundLeg.CarrierIds[i])
  flights$InboundLeg.CarrierIds[i]<-get_carrier(carrier,flights$InboundLeg.CarrierIds[i])
  
}
```

# MNB

``` r
require(httr)
cookies = c(
  '_ga' = 'GA1.2.1046633689.1670507020',
  '_gid' = 'GA1.2.1319713889.1670507020',
  'LBSESSSION' = '!xMVSLdvkoDuv5UPLizWREpXk4TP/dI9T+bB7oCQUGZCdRkk2Ydjbo2SPMgU9NmkwvtYshYkundZP4A==',
  'TS01db72bd' = '012f7c1fff48aa87738362c80cf548ad2c7c70f7897275dac15eef50188540a0e78b5b98db4fd45eff7263c5aa289e041e2cf7de9550d2a8bc6c3d1445bfdbbaa35b0c52cc'
)
headers = c(
  `Accept` = 'application/xml, text/xml, */*; q=0.01',
  `Accept-Language` = 'hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7',
  `Connection` = 'keep-alive',
  `Content-Type` = 'text/xml; charset="UTF-8"',
  `Origin` = 'https://fiokesatmkereso.mnb.hu',
  `Referer` = 'https://fiokesatmkereso.mnb.hu/web/index.html',
  `SOAPAction` = 'http://tempuri.org/IAtmService/GetAtmsAndBranches',
  `Sec-Fetch-Dest` = 'empty',
  `Sec-Fetch-Mode` = 'cors',
  `Sec-Fetch-Site` = 'same-origin',
  `User-Agent` = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
  `X-Requested-With` = 'XMLHttpRequest',
  `sec-ch-ua` = '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
  `sec-ch-ua-mobile` = '?0',
  `sec-ch-ua-platform` = '"Linux"'
)
data = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">\n<s:Body>\n<GetAtmsAndBranches xmlns="http://tempuri.org/">\n<value>\n<entity_list_request>\n  <attributes>\n    <fiok>1</fiok>\n    <atm>1</atm>\n    <am_megk>0</am_megk>\n    <am_haszn>0</am_haszn>\n    <postak>0</postak>\n  </attributes>\n  <coordinates>\n    <lefttop>\n      <lat>51.06963706805956</lat>\n      <lon>14.77856138100921</lon>\n    </lefttop>\n    <rightbottom>\n      <lat>44.371692717851815</lat>\n      <lon>19.052243021634208</lon>\n    </rightbottom>\n  </coordinates>\n  <intezmenyek>\n  </intezmenyek>\n  <limit>\n    <from>1</from>\n    <to>5225</to>\n  </limit>\n</entity_list_request>\n</value>\n</GetAtmsAndBranches>\n</s:Body>\n</s:Envelope>'
res <- httr::POST(url = 'https://fiokesatmkereso.mnb.hu/WcfPublicInterfaceForAtm/AtmService/AtmService.svc/GetAtmsAndBranches', httr::add_headers(.headers=headers), httr::set_cookies(.cookies = cookies), body = data)
str(content(res, 'text'))
# Load the library xml2
library(xml2)
# Read the xml file
mnb_xml <- read_xml(content(res, 'text'))
library(XML)
mnb <- xmlToList(content(res, 'text'))
my_df <- 
  rbindlist(lapply( mnb$Body$GetAtmsAndBranchesResponse$GetAtmsAndBranchesResult$entity_list_response, function(x){
    return(cbind(data.frame(x$attributes[x$attributes!='NULL']), data.frame(x$location[x$location!='NULL']), data.frame(x$coordinates[x$coordinates!='NULL'])))
    
  }), fill = T)
my_df$center.lon <- as.numeric(substring(my_df$center.lon,1,9))*10
my_df$center.lat <- as.numeric(substring(my_df$center.lat,1,9))*10
saveRDS(my_df, 'clean_data.rds')
library(leaflet)
leaflet(my_df) %>% addTiles() %>%
  addMarkers(~as.numeric(center.lon), ~as.numeric(center.lat),
             popup = ~paste(sep = "<br/>", as.character(varos), as.character(megye) )) 
```

``` r
library(RSelenium)
library(rvest)
library(xml2)
rs_driver_obj <- rsDriver(browser = 'chrome', chromever = '106.0.5249.61', port = as.integer(14865))
remDr <- rs_driver_obj$client
remDr$navigate('https://www.bbc.com/')
# remDr$setWindowSize(width = 800, height = 300)
#accept all the cookies
Sys.sleep(25)
webElem <- remDr$findElement("css", "body")
for (i in 1:5) {
  webElem$sendKeysToElement(list(key = "page_down"))
  Sys.sleep(4)
}
remDr$navigate('https://www.cnbc.com/business/')
#accept all the cookies
Sys.sleep(25)
webElem <- remDr$findElement("css", "body")
for (i in 1:5) {
  webElem$sendKeysToElement(list(key = "end"))
  t_b <- remDr$findElement("css", '.LoadMoreButton-loadMore')
  t_b$clickElement()
  Sys.sleep(4)
}
t_page <- remDr$getPageSource()
t <- read_html(t_page[[1]])
t %>% html_nodes('.Card-title') %>% html_text()
write_html(t, 'cnbc.html')
```