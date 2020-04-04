

library(Rfacebook)


# setup Facebook authentication and save taken for future use
#------------------------------------------------------------
# app_id     <- "771608309626862"
# app_secret <- "7c22490a91a9cd7c32fd480b0cabdd53"
# 
# fb_oauth <- fbOAuth(app_id, app_secret, extended_permissions = TRUE)
# save(fb_oauth, file="fb_oauth")

p <- getPage("affinbankberhad", token=fb_oauth)
