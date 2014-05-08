# The Smartsheet to DucuSign Integration

The application connects [Smartsheet](http://www.smartsheet.com) to [DocuSign](http://www.docusign.com) so that users can send the Smartsheet attachments to DocuSign to get the sign from collaborators.

The application is built with Play Framework 2.2.2

## Demo Application
The [SmartSign Demo App](http://smartsheet-docusign.herokuapp.com) is running in Heroku 

## App Demo Screencast
The screencast can be viewed here [Demo Screencast](http://screencast.com/t/uNiVx4xXJFP)

## Configuration
The application needs the following configurations to work properly.

* Database set up
	* By default the application uses H2 database, no need to configure any database to run the applicaiton.
	* To use Postgresql
		* Create new database called "smartsheet-docusign".
		* Configure database database driver, url, user and password in the conf/application.conf.
* Smartsheet set up
	* Added a few attachments to the Smartsheet rows.
	* Added shares to the Smartsheet sheet with collaboratoring users.
	* To use this applicaiton, users need to sign into the applicaiton with Smartsheet credential through Smartsheet OAuth.
		* Create new app in the `Smartsheet Account -> Smartsheet Developer Tool`, memo the following Smartsheet OAuth parameters. The application is set to receive OAuth callback at /oauthCallback, please configure the redirect URL to send OAuth response to <app-base-rul>/oauthCallback.
		* SMARTSHEET_CLIENT_ID=<your-client-id>
		* SMARTSHEET_CLIENT_SECRET=<your-client-secret>
		* SMARTSHEET_REDIRECT_URL=http://localhost:9000/oauthCallback
* DocuSign set up
	* Create the DocuSign integrator key at the `DocuSign Preferences -> Account Administration -> API`, memo integrator key.
		* DOCUSIGN_INTEGRATOR_KEY=<your-integration-key>
	* DocuSign authenticating user set up
		* The application uses DocuSign On-Behalf-Of feature to interact with DocuSign. The authenticating user sends messages on behalf of a regular user. In this way, regular users don't need to sign into DocuSign. Configure an authenticating user based on the instructions in [DocuSign Rest API](https://www.docusign.com/p/RESTAPIGuide/RESTAPIGuide.htm#SOBO/Send On Behalf Of Functionality in the DocuSign REST API.htm%3FTocPath%3D_____3), memo DocuSign authenticating user email and password.
		* DOCUSIGN_AUTH_EMAIL=<dosusign-auth-user-email>
		* DOCUSIGN_AUTH_PASSWORD=<docusign-auth-user-password>
	
	* DocuSign Connect set up.
		* The application relys on DocuSign Connect to receive the status of document being signed. Please set up DocuSign Connect for your environment based on the instructions in [DocuSign Connect](https://10226ec94e53f4ca538f-0035e62ac0d194a46695a3b225d72cc8.ssl.cf2.rackcdn.com/connect-guide.pdf)
	* Add some users to DocuSign, this is not required to run this application.
 	
## Running Locally

First install [Play Framework 2](http://www.playframework.com/documentation/2.2.x/Installing) if yout don't have.

By default the application is configured to use H2 database, so no need to configure database. Export environment variables for Smartsheet and DocuSign in the shell.
	
	$ export SMARTSHEET_CLIENT_ID=<your-client-id>
	$ export SMARTSHEET_CLIENT_SECRET=<your-client-secret>
	$ export SMARTSHEET_REDIRECT_URL=http://localhost:9000/oauthCallback
	
	$ export DOCUSIGN_AUTH_EMAIL=<dosusign-auth-user-email>
	$ export DOCUSIGN_AUTH_PASSWORD=<docusign-auth-user-password>
	$ export DOCUSIGN_INTEGRATOR_KEY=<your-integration-key>
	
Unzip the Play project zip file. And type `play` inside the project folder, then type `run`

	$ unzip smartsheet-docusign.zip
	$ cd smartsheet-docusign
	$ play
	$ [smartsheet-docusign] $ run
	
The application runs in port 9000, go to http://localhost:9000 in the browser.

When the applicaiton runs first time, please click `Apply this script now!` in the browser, this creates database tables the application needs. 

Please click `Sign in` button to use the application.

To change to Postgresql database, configure database driver, URL, username and password in the conf/application.conf. Typicaly URL for local Postgresql like this jdbc:postgresql://localhost:5432/smartsheet-docusign. The smartsheet-docusign is the database name.

	db.default.driver=org.postgresql.Driver
	db.default.url=<your-db-url> 
	db.default.user=<your-db.username>
	db.default.password=<your-db-password>
	
## Running at Heroku

First follow the instructions [Deploy Play Framework to Heroku](http://www.playframework.com/documentation/2.2.x/ProductionHeroku) to create Play application for Heroku.

Heroku uses DATABASE_URL environment variable to configure database. Comment out any database configuration in the conf/applicaiton.conf. After git push heroku master, Heroku creates Postgresql database and exports DATABASE_URL by default, so no need to do any thing. Just make sure the database settings in the conf/application.conf are `commented out with # character`!
Export Smartsheet and DocuSign configuraion to Heroku environment.
	
	// create the Play application based on the URL above.
	
	// set configurations for Smartsheet
	$ heroku config:set SMARTSHEET_CLIENT_ID=<your-client-id>
	$ heroku config:set SMARTSHEET_CLIENT_SECRET=<your-client-secret>
	$ heroku config:set SMARTSHEET_REDIRECT_URL=http://<app-base-url>/oauthCallback
	
	// set configurations for DocuSign
	$ heroku config:set DOCUSIGN_AUTH_EMAIL=<dosusign-auth-user-email>
	$ heroku config:set DOCUSIGN_AUTH_PASSWORD=<docusign-auth-user-password>
	$ heroku cofnig:set DOCUSIGN_INTEGRATOR_KEY=<your-integration-key>
	
	// open heroku application in the browser
	$ herok open


## My Implementations
There are a few subtle conditions while building this application. I made my best decision based on the forum discussion.

* Subject of sign request email
	* The requirement doesn't mention about subject. I added subject input in the confirm dialog page because the subject is required in DocuSign signature request. Users are required to type in subject before submitting.
* Recipient without name
	* There can be case recipient without name. For example when emails are extracted from the sheet, it will be difficult to get name. Also user profile may not have user name. But the DocuSign signature request requires both user name and email. So in the recipient select page, only recipient with name and email can be added.

## Libraries and Modifications
The two main libraries are used to interact with Smartand and DocuSign. The these libraries lack a few features this application needs, so I added or modified to make this applicaiton work. The modified jar files are included in project/lib folder with source jars.

* [Smartsheet Java SDK](https://github.com/smartsheet-platform/smartsheet-java-sdk)
	* The attachFile() method in the AssociatedAttachmentResources does not work, so I fixed it.
* [DocuSign Signature API](https://github.com/docusign/eSignJavaLib)
	* This library does not have On-Behalf-Of feaure, so I added it.
	* I added DocuSignClient.reqeustSignatureFromDocumentURLs() to send a Smartsheet attachment to DocuSign from attachment URL.
	* I added DocuSignClient.getEnvelopeDocument() method to download the signed copy from DocuSign.


Thank you very much

peakpado

