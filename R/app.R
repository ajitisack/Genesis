#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that draws a histogram
library(shiny)
library(shinydashboard)


library(data.table)
library(quantmod)

#source("functions_0.1.R")

nse_eq_url <- "https://www.nseindia.com/content/equities/EQUITY_L.csv"
symbols <- fread(nse_eq_url)[SERIES == "EQ"]

## Sidebar content
sidebar <- sidebarMenu(
		  menuItem("NSE symbols", tabName = "viewsymbols")
		, menuItem("NSE hist data", tabName = "data"
			 , menuSubItem("Download from google", tabName = "downloaddata")
			 , menuSubItem("Load from local file", tabName = "getdata")
		)
		, menuItem("View latest data by price slab", tabName = "viewdatabyprice")
	)

ui <- dashboardPage(
	dashboardHeader(title = "Genesis"),
	dashboardSidebar(sidebar),
	dashboardBody(
		fluidRow(column(12, (DT::dataTableOutput("symbols"))))
	)
)



# Define server logic required to draw a histogram
server <- function(input, output){
	output$symbols <- DT::renderDataTable(
	        DT::datatable(symbols, options = list(pageLength = 20, searching = T))
	)
}


# Run the application
shinyApp(ui, server)

