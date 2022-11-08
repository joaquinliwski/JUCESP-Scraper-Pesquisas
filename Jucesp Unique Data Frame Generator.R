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
write.csv(datautf8,file='C:/Users/Joaquin/Desktop/JUCESP-Scraper-Pesquisas/JUCESP_utf8.csv',row.names=FALSE,fileEncoding = "LATIN1")

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