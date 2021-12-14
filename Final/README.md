# Retailiot - The Smart Clothing Lock
Patricio Reyes, Mayur Bhandary, Aman Prasad
## Overview
The rise of e-commerce has been a growing threat to in-person shopping for over a decade, and the current pandemic has only exacerbated the situation for traditional offline retail stores. Despite the convenience of online shopping, customers are still frustrated with the experience of buying clothing online. Important properties of clothing such as size, texture, and quality cannot be communicated digitally. When users receive a product that doesn't fit them correctly or is not what they expected, the burden of returning the item is bestowed upon them. Furthermore, only a few e-commerce giants and retailers are capable of constructing a supply chain that can promise reasonable delivery times and free returns. For these reasons, we decided to build a checkout experience that augments the in-person shopping experience with a mobile checkout flow. Users can use our device to purchase clothing without speaking to a representative or waiting in line at a checkout counter.  

Retailiot is a smart clothing lock for mobile checkouts at shopping racks. The device uses a motorized locking mechanism to pierce the article of clothing with a needle in order to attach itself. Once the device is attached, it can only be unlocked when a customer purchases it. Customers can interact with the device directly by using a mobile app to scan the device via NFC and pay for it with their prefered payment method. The purpose of this device is to reduce checkout times at retail stores and make it easier for merchants to secure their products.  

## System Diagram
<img src="./images/diagram.jpg">

The system consists of the device, an app, a database, and a backend. Each smart lock has an NFC tag that stores the id for the device. When the user scans the device with the app, the app retrieves product information from the database for the id that was scanned. After the user completes the checkout flow with their preferred payment method, the app sends a GET request to the backend hosted on Heroku to unlock the device. The backend publishes a message to an MQTT topic that the device is subscribed to which signals the device to unlock itself. 

## Storyboard
<img src="./images/story-board1.png">
<img src="./images/story-board2.png">
<img src="./images/story-board3.png">
<img src="./images/story-board4.png">

## Prototyping

<img src="./images/rough_prototype.png">
Our first iteration of the device was very crude. We used this to determine whether a servo motor and safety pin would be strong enough to secure the clothing. After experimenting on a sock, we determined that this mechanism should be sufficient for our prototype.  

<img src="./images/prototype.gif">
We also used cardboard to create a full functional prototype of our device and collect feedback. The device is shaped like a tile with a slit across the corner to insert clothing. Since we used the servo moter to actuate the needle, we created another slit to allow the motor arm to move freely when locking and unlocking the device. 


## Code


#### Device:
- The device code can be found in the files smart_lock.py and text_draw.py. The smart_lock.py script simply subscribes to an MQTT topic corresponding to its device id ('123' was used for our prototype device) and moves the servo arm when it receives the lock and unlock messgages. '1' was used to lock the device and '0' was used to unlock it. The text_draw.py script was used to display text on the device screen. 

#### Backend:
- The backend utilzes FastAPI to create an API wrapper for the MQTT publishing functions. The software is deployed to Heroku such that it can be accessed via the mobile application. When the mobile application sends a request to the API to toggle the lock for a particular device, the server issues an MQTT message to that device. We plan to expand this backend to incorporate a database system that links devices to products, and also completes payments. The goal is to trigger an unlock once a payment is successfully completed, and to trigger a lock once the merchant decides to secure the lock.

#### App:
- The app (written in Swift), scans an NFC tag that lives on the lock, and uses that to pull up information about the product that the lock is secured to. The user is then able to use the app to "pay" for the product, subsequently releasing the product from the lock. In the future, we aim to request the product information from the backend (which will pull product information from the database). We also aim to incorporate the payment system, along with a "cart" mechanic which would allow shoppers to purchase multiple products at once.

## Open Studio 
<img src="./images/open_studio.jpg">

We participated in open studio to demonstrate our project and get feedback from attendees. Overall, the device was well received and the participants felt that they could see themselves using it to checkout at retail stores. 

One question that we repeatedly received was what does the user do with the device after it has been unlocked? Our suggestion was to have baskets to drop the unlocked devices into. The attendees seemed satisfied with this answer, but we acknowledge that this makes the experience a bit clunkier. An alternative that we thought through was to eliminate the device for cheaper items and introduce the NFC sticker to the existing tags on the clothing. This would allow on the spot checkout without the device, but it would not have the added security of a clothing lock. One attendee suggested that we target high end retailers who frequently use heavy duty clothing locks with their premium products. 

Other feedback included interaction nuances, technical challenges, and ethical considerations:
- If a customer purcheses many items at once, it might become annoying to self-checkout each one. 
- Some clothing manufacturers take packaging very seriously. The aesthetics of the lock will be very important in gaining adoption. 
- The existing RFID tags on clothes would still be necessary in order to trigger the alarm at the door for unpaid goods. 
- This product might eliminate cashier jobs. 

<img src="./images/render1.png">
<img src="./images/render2.png">
<img src="./images/poster1.png">
<img src="./images/poster2.png">

We generated high fidelity concept prototypes of our envisioned device. Our design draws inpiration from popular tag-like devices such as Tile and AirTags.   


