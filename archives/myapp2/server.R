source('app1fun.R')

bsels <- bse.readScriptList()

fixedrange <- list("Last 1 day"="1d", "Last 5 days"="5d", "Last 10 days"="10d", "Last 15 days"="15d",
                   "Last 1 month"="1m", "Last 3 months"="3m", "Last 6 months"="6m", "Last 9 months"="9m",
                   "Last 1 year"="1y", "Last 2 years"="2y", "Last 3 years"="3y")

function(input, output) {
    output$company <-renderUI({
        if(input$industry=="<ALL>"){
            x <- bsels[,c("name")]
            y <- bsels[,c("id")]
        } else {
            x <- bsels[bsels$industry == input$industry,c("name")]
            y <- bsels[bsels$industry == input$industry,c("id")]
        }
        names(y) <- x
        selectInput("company", label=h5("Company"), choices = y, width = "400px")
    }) #renderUI
    output$rangeValue <- renderUI({
        if (is.null(input$rangeType)) return()
        switch(input$rangeType,
               "f" = selectInput("rangeValue", h5("Select Period"), choices=fixedrange),
               "d" = sliderInput("rangeValue", h5("No. of days"), min=1, max=15, value=1, step=1, ticks=T),
               "m" = sliderInput("rangeValue", h5("No. of months"), min=1, max=36, value=1, step=1, ticks=T),
               "y" = sliderInput("rangeValue", h5("No. of years"), min=1, max=3, value=1, step=1, ticks=T)
        )
    })
    output$chart <- renderPlot({
        if (is.null(input$company) | is.null(input$rangeType) | is.null(input$rangeValue)) return()
        if (input$rangeType == "f" & is.integer(input$rangeValue)) return()
        range <- if (input$rangeType=="f") input$rangeValue else paste(input$rangeValue, input$rangeType, sep="")
        if (gsub("[0-9]","", range) %in% c("d","m","y"))
        yahoo.plotBseEquityData(symbol=input$company, plottype=input$plottype, range=range)
        if (input$action) addSMA(n=as.numeric(input$period))
    }) #renderPlot
    output$table <- renderDataTable({
        if (is.null(input$company) | is.null(input$rangeType) | is.null(input$rangeValue)) return()
        range <- if (input$rangeType=="f") input$rangeValue else paste(input$rangeValue, input$rangeType, sep="")
        yahoo.getBseEquityData(symbol=input$company, range=range)
    }) #renderDataTable
}
