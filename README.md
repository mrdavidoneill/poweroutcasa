# Email checker

## Description

A Python service to use your Gmail account to regularly check that a status email was received, which when used in conjunction with a regular email sender, such as https://github.com/mrdavidoneill/emailer, or those found on ISP routers, forms the basis of a system health check. eg. to make sure your house/office has not had a power cut.

- Deletes emails older than 12 mins, to not use up your mailbox space
- Logs errors to file and debug info to the console
- NOTE: Use cronjob to run the program at an interval equal to your email sender

## Story behind the project

Often here, power cuts are experienced, and so I needed a simple way to keep a check on the place when away. As my home router sent emails at regular intervals, I wrote this script to check emails were received, and remove older emails.
