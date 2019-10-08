library(shiny)
library(quantmod)

source('app1fun.R')

bsels <- bse.readScriptList()
industryList <- as.list(sort(unique(bsels$industry)))
industryList[[length(industryList)+1]] <- industryList[[1]]
industryList[[1]] <- "<ALL>"
plotType <- list("Line Chart"="l", "Bar Chart"="b", "CandleStick"="c")
rangetype <- c("Fixed Period"="f", "Day"="d", "Month"="m", "Year"="y")
ind <- list("SMA" = 1)


fluidPage(
    titlePanel(h3("BSE Chart")),
    fluidRow(
        column(3, selectInput("industry", label=h5("Industry"), choices=industryList)),
        column(6, uiOutput("company"))
    ), #fluidRow

    fluidRow(
        column(3, selectInput("plottype", label=h5("Plot type"), choices=plotType)),
        column(2, radioButtons("rangeType", label = h5("Date range unit"), choices = rangetype)),
        column(2, uiOutput("rangeValue"))
    ),

    tabsetPanel(
        tabPanel("Plot",
            column(3,
                checkboxGroupInput("indicator", label = h5("Indicators"), choices=ind ,selected = 1),
                textInput("period", label = h5("Period")),
                actionButton("action", label = "Action")
            ),
            column(9,plotOutput("chart"))
        ),
        tabPanel("Table", dataTableOutput("table"))
    ) #tabsPanel
)
