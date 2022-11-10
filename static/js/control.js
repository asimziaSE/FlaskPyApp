$(function () {
    var reportContainer1 = $("#report-container1").get(0);

    // Initialize iframe for embedding report
    powerbi.bootstrap(reportContainer1, { type: "report" });

    var models = window["powerbi-client"].models;
    var reportLoadConfig = {
        type: "report",
        tokenType: models.TokenType.Embed,

        // Enable this setting to remove gray shoulders from embedded report
        settings: {
            panes: {
                filters: {
                    visible: false
                },
                pageNavigation: {
                    visible: false
                }
            }
        }
    };
    

    $.ajax({
        type: "GET",
        url: "/getembedinfo",
        dataType: "json",
        success: function (data) {
            embedData = $.parseJSON(JSON.stringify(data));
            reportLoadConfig.accessToken = embedData.accessToken;

            // You can embed different reports as per your need
            reportLoadConfig.embedUrl = embedData.reportConfig[2].embedUrl;
            

            // Use the token expiry to regenerate Embed token for seamless end user experience
            // Refer https://aka.ms/RefreshEmbedToken
            tokenExpiry = embedData.tokenExpiry;

            // Embed Power BI report when Access token and Embed URL are available
            var report1 = powerbi.embed(reportContainer1, reportLoadConfig);
            

            // Triggers when a report schema is successfully loaded
            report1.on("loaded", function () {
                console.log("Report load successful")
            });
            

            // Triggers when a report is successfully embedded in UI
            report1.on("rendered", function () {
                console.log("Report render successful")
            });
            
            window.setInterval(function () {
                report1.refresh();
            }, 10 * 1000);

            // Clear any other error handler event
            report1.off("error");

            // Below patch of code is for handling errors that occur during embedding
            report1.on("error", function (event) {
                var errorMsg = event.detail;

                // Use errorMsg variable to log error in any destination of choice
                console.error(errorMsg);
                return;
            });
        },
        error: function (err) {

            // Show error container
            var errorContainer = $(".error-container");
            $(".embed-container").hide();
            errorContainer.show();

            // Format error message
            var errMessageHtml = "<strong> Error Details: </strong> <br/>" + $.parseJSON(err.responseText)["errorMsg"];
            errMessageHtml = errMessageHtml.split("\n").join("<br/>")

            // Show error message on UI
            errorContainer.html(errMessageHtml);
        }
    });
});