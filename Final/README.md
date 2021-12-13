# Retailiot - The Smart Clothing Lock

## Overview
Retailiot is a smart clothing lock for mobile checkouts at retail stores. The device uses a motorized locking mechanism to pierce the article of clothing with a needle in order to attach itself. Once the device is attached, it can only be unlocked when a customer purchases it. Customers can interact with the device directly by using a mobile app to scan the device via NFC and pay for it with their prefered payment method. The purpose of this device is to reduce checkout times at retail stores and make it easier for merchants to secure their products.  

## System Diagram
<img src="./images/diagram.jpg">

The device uses MQTT to facilitate communications between the device and the mobile app. Each smart lock has an NFC tag that stores the id for the device. When the user scans the device with with the app, the app retrieves product information from the database for the id that was scanned. When the user completes the checkout flow with their preferred payment method, the app sends a GET request to the backend hosted on Heroku to unlock the device. The backend publishes a message to an MQTT topic that the device is subscribed to which signals the device to unlock itself. 

## Prototype
<img src="./images/prototype.gif">

## Open Studio 
<img src="./images/open_studio.jpg">

<img src="./images/render1.png">
<img src="./images/render2.png">
<img src="./images/poster1.png">
<img src="./images/poster2.png">


