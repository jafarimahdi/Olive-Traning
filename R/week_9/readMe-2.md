-   <a href="#coindesk" id="toc-coindesk">Coindesk</a>
-   <a href="#infoworld-scraper" id="toc-infoworld-scraper">Infoworld
    scraper</a>
-   <a href="#yachtworld-scraper" id="toc-yachtworld-scraper">Yachtworld
    scraper</a>

``` r
library(rvest)
library(data.table)
```

Typical HTML process task:

-   Create a function that will process one page and return with a data
    frame with one line
-   Create the links that you want to process, you also can write a
    function that will extract the links first then save them into a
    vector
-   `lapply` your function to your links, you will get a list of data
    frames
-   `rbindlist` your result into one dataframe

# Coindesk

``` r
t <- read_html('https://www.coindesk.com/tag/bitcoin/')
title <- 
t %>% 
  html_nodes('.card-title') %>% 
  html_text()
link <- 
paste0('https://www.coindesk.com',
  t %>% 
  html_nodes('.card-title') %>%
  html_attr('href')
)
teaser <- 
t %>% 
  html_nodes('.content-text') %>% 
  html_text()
  
df <- data.frame('title' = title, 'link'= link, 'teaser'= teaser)
get_coindesk_one_page <- function(url) {
  t <- read_html(url)
  
  title <- 
  t %>% 
    html_nodes('.card-title') %>% 
    html_text()
  
  link <- 
  paste0('https://www.coindesk.com',
    t %>% 
    html_nodes('.card-title') %>%
    html_attr('href')
  )
  
  teaser <- 
  t %>% 
    html_nodes('.content-text') %>% 
    html_text()
    
  df <- data.frame('title' = title, 'link'= link, 'teaser'= teaser)
  return(df)
}
links <- paste0('https://www.coindesk.com/tag/bitcoin/', 1:5, '/')
list_of_pages <- lapply(links, get_coindesk_one_page)
df <- rbindlist(list_of_pages)
```

# Infoworld scraper

``` r
url <- 'https://www.infoworld.com/category/data-science/'
get_one_page <- function(url) {
  print(url)
  t <- read_html(url)
  
  boxes <- t %>% html_nodes('.river-well')
  
  list_of_boxes <- lapply(boxes, function(x){
    
  title <- 
    x%>% 
      html_nodes('.post-cont a')%>%
      html_text() 
    
    
  relative_link <- 
    x%>% 
      html_nodes('.post-cont a')%>%
      html_attr('href')
  
  link <- paste0('https://www.infoworld.com', relative_link)
  
  teaser <-
    x  %>%
      html_nodes('h4')%>%
      html_text()
  #
    return(data.frame('title'= title, 'teaser'= teaser, 'link'= link))
  #
  })
  one_page <- rbindlist(list_of_boxes) 
 return(one_page)
}  
df <- get_one_page(url = url)
```

    ## [1] "https://www.infoworld.com/category/data-science/"

``` r
links <- paste0('https://www.infoworld.com/napi/tile?def=loadMoreList&pageType=index&catId=3781&category=3781&includeMediaResource=true&createdTypeIds=1&categories=%5B3781%5D&days=-730&pageSize=20&offset=0&ignoreExcludedIds=true&brandContentOnly=false&includeBlogTypeIds=1%2C3&includeVideo=true&liveOnly=true&sortOrder=date&locale_id=0&startIndex=',seq(0,60, 20)  )
list_of_dfs<- lapply(links, get_one_page)
```

    ## [1] "https://www.infoworld.com/napi/tile?def=loadMoreList&pageType=index&catId=3781&category=3781&includeMediaResource=true&createdTypeIds=1&categories=%5B3781%5D&days=-730&pageSize=20&offset=0&ignoreExcludedIds=true&brandContentOnly=false&includeBlogTypeIds=1%2C3&includeVideo=true&liveOnly=true&sortOrder=date&locale_id=0&startIndex=0"
    ## [1] "https://www.infoworld.com/napi/tile?def=loadMoreList&pageType=index&catId=3781&category=3781&includeMediaResource=true&createdTypeIds=1&categories=%5B3781%5D&days=-730&pageSize=20&offset=0&ignoreExcludedIds=true&brandContentOnly=false&includeBlogTypeIds=1%2C3&includeVideo=true&liveOnly=true&sortOrder=date&locale_id=0&startIndex=20"
    ## [1] "https://www.infoworld.com/napi/tile?def=loadMoreList&pageType=index&catId=3781&category=3781&includeMediaResource=true&createdTypeIds=1&categories=%5B3781%5D&days=-730&pageSize=20&offset=0&ignoreExcludedIds=true&brandContentOnly=false&includeBlogTypeIds=1%2C3&includeVideo=true&liveOnly=true&sortOrder=date&locale_id=0&startIndex=40"
    ## [1] "https://www.infoworld.com/napi/tile?def=loadMoreList&pageType=index&catId=3781&category=3781&includeMediaResource=true&createdTypeIds=1&categories=%5B3781%5D&days=-730&pageSize=20&offset=0&ignoreExcludedIds=true&brandContentOnly=false&includeBlogTypeIds=1%2C3&includeVideo=true&liveOnly=true&sortOrder=date&locale_id=0&startIndex=60"

``` r
final_df <- rbindlist(list_of_dfs)
head(final_df,1)
```

    ##                                                           title
    ## 1: 5 modelops capabilities that boost data science productivity
    ##                                                                                                                                                  teaser
    ## 1: Organizations are hiring data scientists to develop ML models and experiment with AI, but the business impact is lagging for many large enterprises.
    ##                                                                                                           link
    ## 1: https://www.infoworld.com/article/3677368/5-modelops-capabilities-that-boost-data-science-productivity.html

# Yachtworld scraper

The base url is <https://www.yachtworld.co.uk/boats-for-sale/>

``` r
# scraper for one page 
url <- 'https://www.yachtworld.co.uk/yacht/2021-ryck-280-8036770/'
t_list <- list()
t <- read_html(url)
t_list[['title']] <- t %>% html_node('.heading') %>% html_text()
t_list[['length']] <- t %>% html_nodes('.boat-length') %>% html_text()
t_list[['price']] <- t %>% html_nodes('.payment-total') %>% html_text()
t_list[['location']] <- t %>% html_node('.location') %>% html_text()
keys <- t %>% html_nodes('.datatable-title') %>% html_text()
values <- t %>% html_nodes('.datatable-value') %>% html_text()
if (length(keys)==length(values)) {
  for (i in 1:length(keys)) {
    t_list[[keys[i]]] <- values[i]
  }
}
get_one_yachts  <- function(url) {
  t_list <- list()
  
  t <- read_html(url)
  t_list[['title']] <- t %>% html_node('.heading') %>% html_text()
  t_list[['length']] <- t %>% html_nodes('.boat-length') %>% html_text()
  t_list[['price']] <- t %>% html_nodes('.payment-total') %>% html_text()
  t_list[['location']] <- t %>% html_node('.location') %>% html_text()
  
  
  keys <- t %>% html_nodes('.datatable-title') %>% html_text()
  values <- t %>% html_nodes('.datatable-value') %>% html_text()
  if (length(keys)==length(values)) {
    for (i in 1:length(keys)) {
      t_list[[keys[i]]] <- values[i]
    }
  }
  return(t_list)
}
```

``` r
links <- c('https://www.yachtworld.co.uk/yacht/2019-jeanneau-nc-37-8469810/',
           'https://www.yachtworld.co.uk/yacht/2022-bestevaer-53-motoryacht-8218108/',
           'https://www.yachtworld.co.uk/yacht/1986-motor-yacht-38m-nicolini-8569109/')
data_list <- lapply(links, get_one_yachts)
df <- rbindlist(data_list, fill = T)
```