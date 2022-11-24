################################################################################
#                       JUCESP Pesquisa                                        #
#               Unique Data Frame & Plots/Tables                               #
################################################################################
rm(list=ls())

#Load Packages
suppressMessages({
  if(!require("pacman")) install.packages("pacman")
  pacman::p_load("tidyverse","haven")
})

#Merge UTF-8
setwd("C:/Users/Joaquin/Desktop/JUCESP-Scraper-Pesquisas/utf8") 
datautf8<-list.files()%>%lapply(function(i){
  read.csv(i,sep=",",colClasses=c(NIRE="character"))%>%distinct()
})%>% bind_rows()
#datautf8<-lapply(datautf8,iconv, from = 'UTF-8', to = 'ASCII//TRANSLIT')

datautf8<-datautf8%>%mutate_if(is.character, 
                               function(col) iconv(col, from = 'UTF-8', to='ASCII//TRANSLIT'))%>%distinct()


data_00_10<-datautf8%>%filter(Year<=2010)
write.csv(data_00_10,file='C:/Users/Joaquin/Desktop/JUCESP-Scraper-Pesquisas/JUCESP_00_10.csv',row.names=FALSE,fileEncoding = "LATIN1")
data_11_20<-datautf8%>%filter(Year>2010,Year<=2020)
write.csv(data_11_20,file='C:/Users/Joaquin/Desktop/JUCESP-Scraper-Pesquisas/JUCESP_11_20.csv',row.names=FALSE,fileEncoding = "LATIN1")
data_21_22<-datautf8%>%filter(Year>2020,Year<=2022)
write.csv(data_21_22,file='C:/Users/Joaquin/Desktop/JUCESP-Scraper-Pesquisas/JUCESP_21_22.csv',row.names=FALSE,fileEncoding = "LATIN1")



#Merge Latin1
#setwd("C:/Users/Joaquin/Desktop/JUCESP-Scraper-Pesquisas/latin1") 
#datalatin1<-list.files()%>%lapply(function(i){
#  read.csv(i,sep=",",colClasses=c(NIRE="character"),fileEncoding = "LATIN1")%>%distinct()
#})%>% bind_rows()
#municiplatin1<-datalatin1%>%select(NIRE,Município,MunicÃ.pio)%>%unite('Município', Município:MunicÃ.pio, remove=T, na.rm = TRUE)
#datalatin1<-datalatin1%>%select(-Município,-MunicÃ.pio)
#datalatin1<-full_join(datalatin1,municiplatin1)%>%distinct()
#write.csv(datalatin1,file='C:/Users/Joaquin/Desktop/JUCESP-Scraper-Pesquisas/JUCESP_latin1.csv',row.names=FALSE,fileEncoding = "LATIN1")

#antijoin<-anti_join(datautf8,datalatin1)%>%group_by(Month,Year)%>%summarise(n())
#check<-datautf8%>%group_by(Month,Year)%>%summarise(n())

obs9990<-datautf8%>%group_by(Year,Month,Type)%>%summarise(count=n())#%>%filter(count==9900)

dataplot<-datautf8%>%group_by(Month,Year)%>%summarise(count=n())
dataplot$date<-as.Date(paste(dataplot$Year,"-",dataplot$Month,"-01",sep=""))
ggplot(dataplot, aes(x = date, y = count)) +
  geom_line() 