


    ##########################################################################    _*@-TARIFFS-@*_    #############################################################################
    #                                                                                                                                                                            #
    #Thought to myself lets be real, you gotta check for those tariffs. How do most manage to do that? From a cursory google search, by linking APIS. I found one such API that  #
    # tracks tariffs and other export related fun and is updated several times a day. I was about to request a key for access to this API but decided I'm going to just figure   #
    # out how to make it work without actually using the other API. this API will be fully prepared and functional in its link to the De Minimis API.(will link to site below)   #
    # Since you don't need to check for tariffs intranationally, all the testing being done will be using products and users within the US.                                      #
    #                                                                                                                                                                            #
    ##############################################################################################################################################################################
    more on De Minimis API: https://internationaltradeadministration.github.io/developerportal/de-minimis.html


   -----------------------------------------------------------------------------------  @utils:  -----------------------------------------------------------------------------------

    if I learned anything from the advanced python project, one doesn't simply *not* check if a thing being passed around actually has a value before using it. so, where ever
    it makes sense I do a "do I exist?" check. I feel like the lesson did not touch enough on ~~the numbered messages (201, 200, 404 etc)~~ on http status codes (or maybe I
    accidentally skipped that part); but in the vein of writing code that looking similar to the pokemon api code in the study material and other examples I used from the web, I 
    was implementing status codes. the status codes and the "do I exist" checks were cramping things up so bad that I couldn't figure out what I still needed to get done. 
    *SO* I made some helper functions to cut down the repetitive code so that looking at everything would be easier.
     ^^
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                                                                                @BLUEPRINTS@
                                                                                @BLUEPRINTS@
                                                                                @BLUEPRINTS@
                                                                                @BLUEPRINTS@
    ______________________________________________________________~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~________________________________________________________________

    I feel like this was a risky move as the assignment has clear instructions on using create_all(), but I have WAY TOO MANY MODELS for this to be a single paged application
    without risking a heart attack. After app.py quickly became *overwhelming* I knew I needed to give models routes and everything more breathing room and separate things.
    asked the web how to do that effectively and Flasks blueprints were what I found to make this work. and as I continued researching, create_all() is never used in 
    real applications. so, please dont mark me off for this. for the sake of readability!! 



                                                                                @file organization
    I looked around the web for suggestions after deciding I was going to use blueprints. google searched "flask API best practices for file architecture" 
    I looked around for a few hours so there were more that I looked at but these are a few of them:
    https://ashleyalexjacob.medium.com/flask-api-folder-guide-2023-6fd56fe38c00
    https://stackoverflow.com/questions/14415500/common-folder-file-structure-in-flask-app
    https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy

    
    

        