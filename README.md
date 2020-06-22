# FlashStocks Stock Image Site
<img src="https://github.com/jolenewai/flashing-stocks-app/blob/master/static/dev/flashstocks_screenshot.png" style="margin:0">

There are a lot of stock images website available. Most of them requires us to purchase credits upfront in order to get the image we like. There are times where users only needed one or two images and feeling reluctant to purchase credits right at the start. Given this situation, **FlashStocks** is a platform that allows users to purchase stock images that they needed, without having to pay extra. This is also a platform which Photographers are allowed to upload their photos for selling. 
 
You may access the deployed website from [here](https://jw-flashstocks.herokuapp.com/)

## UX/UI
 
### User Stories:
2 major group of users of the website are targeted
- Customers who are looking for images for their website/social media/marketing materials
- Photographers who are looking for a platform to sell their Photographers

Detailed user stories can be accessed [here](https://docs.google.com/spreadsheets/d/1alX_U1jTtiYUDutN3o2Mt0yoms3RqJWCAP7SaGKaSkw/edit?usp=sharing)

### Wireframes

The wireframes and mockup of the website can be accessed here:

[Desktop](https://xd.adobe.com/view/4d1f629b-8bf9-4aae-7838-340428da7a2d-3b2e/?fullscreen) 
- Max 4 columns for the images on larger screenshot
- Searchbar are on top of every page
- 2 columns layout is used on most of the pages

[Mobile](https://xd.adobe.com/view/564f29fa-c2a6-4b32-6725-385a94dfa08d-207e/?fullscreen)
- Due to space constraint, the search bar is collapsed into an icon, it will appear upon clicking the search icon on the navbar
- 2 columns layout will become one column and the container will stack over one another
- Filter for Search Result is hidden and will appear upon clicking the button at the bottom right corner
- Some columns in the tables is hidden due to space constraint


The ER diagrams can be accessed [here](https://github.com/jolenewai/flashing-stocks-app/blob/master/static/dev/flashstocks_er_diagram.png)

### Navigation

- The main way to navigate through the website is through searching 
- User can also explore for images by filtering the images within certain category

### Colour Scheme
<img src="https://github.com/jolenewai/flashing-stocks-app/blob/master/static/dev/UI_Elements_-_Color_Palette.jpg" style="margin:0">

The colour scheme is a combination of vibrant colours and shades of black.

Topbar background color is switched between Mango Tango and Black to differentiate the distinctiveness of user group. Mango Tango is presented to Customers, and black is used for Photographers and admin who are performing mainly backend tasks.


### Typography
- Google Font '[Proza Libre](https://fonts.google.com/specimen/Proza+Libre)' is used for both headers and contents 


## Features

### Existing Features for Customers
#### Landing Page
Greeting users with choice of actions, "Explore", "Login" and "Sign-Up". Users can also choose to start with a search with keyword

#### Home Page
This will display the most recent photos uploaded by photographers

#### User Registration and Authentications
- User can sign-up as __Customers__ or __Photographers__. This will determine the tasks they can perform after login.
- There is also a small section for __Admin__ to manage photo tags and categories.

#### Customers
User can login to perform the following task:
- [x] Create Profile
- [x] View Profile
- [x] Edit Profile
- [x] Favourite a photo and view them back later

#### Shopping Cart
- [x] Add Images to Cart
- [x] Update Size of the images in the Cart
- [x] Delete image from the cart
- [x] Review items and total amount in cart before checking out
- [x] Checkout to complete the purchase

#### Browsing Images
- [x] The Explore page will show all most recent images, they can also browse into category directly with the link under the heading
- [x] Categories are retrieved from the database
- [x] Images that have multiple categories will appear in their respective category page
- [x] Individual photo details is accessible by clicking on the the title or download button which overlay the image upon hovering (or click on mobile) the image itself
- [x] Browsing images by tags is also possible by accessing it from the search page


#### Search
- [x]The search bar is placed on top of every page except that it will be hidden and toggled in mobile layout. In the search bar, user can perform search by entering the keywords for _captions_, _descriptions_ or _tags_. 

On the search result page, user can perform further filtering on the search results by limiting it to a specific  _Category_, users can also change the sorting of the result based on _Most Recent_ or _Alphabetical Order_.


#### View Photographer Profile
User can view a photographer's profile and uploads on the same page


### Photographers
User can login to perform the following task:
- [x] Add a photo
- [x] Edit/update photo
- [x] Delete a photo
- [x] Create an album
- [x] Edit/Update an album
- [x] Delete an album
- [x] View the uploads 
- [x] View the downloads

### Admin
User can login to perform the following task:
- [x] Add a Tag
- [x] Edit/update a Tag
- [x] Delete a Tag
- [x] Add a Category
- [x] Edit/Update a Category
- [x] Delete a Category


#### Features Left to Implement
- [ ] To allow Customers sort by Popularity of the images
- [ ] To allow Photographers to add photos into the albums
- [ ] Lazy loading for the images
- [ ] To allow Customer to follow a Photographer to receive updates upon new uploads
- [ ] Pagination to handle large number of results

## Technologies Used

* HTML 
* CSS
* Javascript 
* [JQuery](https://jquery.com/) to simplify DOM manipulation
* [Bootstrap version 4.4](https://getbootstrap.com/) for toggle of tabs navigation  
* [Django 2.2.6](https://www.djangoproject.com/) as the Framework 
* [Django-allauth](https://django-allauth.readthedocs.io/en/latest/) for user authentications
* [PostgreSQL](https://www.postgresql.org/) for online database solution
* [GitHub](https://github.com/) for versioning control


### Software
* [Adobe XD](https://www.adobe.com/sea/products/xd.html) for wireframing and UI design 
* [Adobe Photoshop](https://www.adobe.com/sea/products/photoshop.html) for photos editing and cropping
* [Adobe Illustrator](https://www.adobe.com/sea/products/illustrator.html) to create site logo


## Plugins

* [Uploadcare API](https://uploadcare.com/) for uploading images on a separate cloud


## Testing

Testing accounts are created to perform the following testing:

### For Customer
```
Username : sophia3344
Password : testing1234
```

### For Photographer
```
Username : WilliamW
Password: testing1234
```

### For Admin
```
Username : admin
Password: abcdefg1234
```

### Manual Testing

#### User Registration
- [x] On the home page, click on Sign-Up
- [x] Try to submit the empty form and verify that error messages about the required fields appear 
- [x] Try to submit the form with an existing email address on the database and verify that the registration will be rejected to preserve the uniqueness of the email in the database


#### Email Verification Upon User Registration / Sign Up
- [x] Try to submit the form with valid data and receive email for verification
- [x] Click on the verification link in the email and click on confirm
- [x] After clicking the confirm button, the page is redirected to login page 


#### Login 
- [x] On the home page, click on Login
- [x] Try to submit the empty form and verify that error messages about the required fields appear
- [x] Try to submit the form with an invalid email address and verify that it is an invalid login
- [x] Try to submit the form with a wrong password and verify that it is an invalid login
- [x] Try to submit the form with all inputs valid and verify that the redirection is successful and on the top bar it changes "Login" to "Logout"


#### Add Items to Cart
- [x] Click on download on any image to access to the image detail page
- [x] Click on the Download button after choosing a size
- [x] Verify that image is added to cart successfully by seeing Message _'Image is added to cart successfully'_ appear on top of the page
- [x] Further verify the image is in the cart by clicking on the _Cart_ icon on the top navigation bar 
- [x] The number of items beside the cart will also be updated upon image added to cart


#### Edit Item in Cart
- [x] Click on _Edit_ button beside the _Size_ of one of the image 
- [x] A modal box with all the sizes available will display
- [x] Verify that the modal box will close after clicking the _Cancel_ button in the modal box
- [x] Click on _Delete_ button beside the _Size_ of one of the image 
- [x] A modal box with confirmation message will display
- [x] Verify that the size is changed after clicking the _Update_ button in the modal box


#### Delete Item in Cart
- [x] Click on _Delete_ button beside the _Size_ of one of the image 
- [x] A modal box with confirmation message will display
- [x] Verify that the modal box will close after clicking the _Cancel_ button in the modal box
- [x] Click on _Delete_ button beside the _Size_ of one of the image 
- [x] A modal box with confirmation message will display
- [x] Verify that the image is deleted after clicking the _Confirm_ button in the modal box


#### Checkout (with valid testing card number)
- [x] Click on the checkout button on _View Cart_ page
- [x] Click on submit button without entering information and verify that error message will appear
- [x] Enter valid information and click on _Pay_ button
- [x] Verify that the checkout is successful after being redirected to a checkout success page, and items are being added to the download history


#### Checkout (with invalid testing card number)
- [x] Click on the checkout button on _View Cart_ page
- [x] Enter invalid testing card number and click on _Pay_ button
- [x] Verify that the checkout cannot proceed and error is displayed


#### Handling illegal checkout by typing of URL 
- [x] To prevent user from directly typing the checkout success url to bypass the payment process and get items purchased, an unique checkout session id is created and will be verified through the URL parameter
- [x] In the address bar, enter https://jw-flashstocks.herokuapp.com/checkout/success and get an error of "Page not found"
- [x] In the address bar, enter https://jw-flashstocks.herokuapp.com/checkout/success/123 and get redirected to View Cart page and display an error message of invalid checkout session id 

#### Add Photo to My Favourite (no login)
- [x] On any image, click on the heart
- [x] Verify that page will be redirected to login page as this action requires login

#### Add Photo to My Favourite (after login as Customer)
- [x] On any image, click on the heart
- [x] Verify that the heart will changed to a heart filled with red colour instead
- [x] Verify that the image is added to favourite by clicking opening My Favourite page in the collapsible side bar 

#### Add A Photo (without login as Photographer)
- [x] In the address bar, type in the url for adding a photo directly
- [x] If the user is not logged in, user will be redirected to login page
- [x] If the user didn't login as Photographer, access to the page will be denied

#### Add A Photo (after login as Photographer) 
- [x] Click on My Uploads on the side navigation, click on Upload button on the right corner of the page
- [x] Try to submit the empty form and verify that error messages about the required fields appear
- [x] Try to submit the form with all inputs valid and verify the review has been added when redirected to My Uploads page

#### Update A Photo 
- [x] On My Upload page, click on the edit icon beside the title of the image
- [x] Verify that information from the database are presented in the form inputs, try to change one of the field and verify that the field is updated after submit the form

#### Delete A Photo
- [x] On My Uploads page, click on the delete icon beside the title of the review
- [x] Verify that confirmation message is displayed and try to press confirm and verify that the review is deleted when redirected to My Uploads page

#### Update Profile
- [x] On Profile page, click on the Update Profile link in under the profile display
- [x] Verify that information from the database are presented in the form inputs, try to change one of the field and verify that the field is updated after submit the form
- [x] Try to change image and submit and verify that the image is updated after submit the form

#### CRUD For Tags
- [x] Create, read, update and delete tags are tested after login as Admin
- [x] Verify that create will add a new tag
- [x] Verify that read will list all the tags in database
- [x] Verify that update will change the selected tag
- [x] Verify that delete will remove the selected tag

#### CRUD For Categories
- [x] Create, read, update and delete categories are tested after login as Admin
- [x] Verify that create will add a new category
- [x] Verify that read will list all the categories in database
- [x] Verify that update will change the selected category
- [x] Verify that delete will remove the selected category

#### Search 
- [x] On any page, type in any keyword in the search bar, verify that the matching results appear in Search Result page
- [x] On Search Result page, apply filter with one of the category and sorting, and verify that the matching results displayed

#### Browsing Images by Category on Explore page
- [x] Click on each button and verify that the matching images are displayed

#### Responsivenesss
This website is responsive on the following devices
- [x] Widescreen Desktop (above 992px)
- [x] Tablet in Landscape (between 768px and 991.98px)
- [x] Mobile Phones (below 576px)

#### HTML validation
All pages are validated with the following website and returns no error (except the page with uploadcare attribute)
- [x] [FREEFORMATTER](https://www.freeformatter.com/html-validator.html)
- [x] [validator.nu](https://html5.validator.nu/)

#### CSS Validation
CSS are validated and return no errors except -webkit- related 
- [x] [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/)


## Deployment

This website is deployed on [Heroku](https://www.heroku.com). 
The URL for the deployed website is https://jw-flashstocks.herokuapp.com/

### Prerequisite for deployment
- [x] An IDE e.g. Visual Studio Code or Gitpod
- [x] Account with [Heroku](https://www.heroku.com)
- [x] Account with [UploadCare](https://uploadcare.com/) for image uploading
- [x] Account with [stripe](https://stripe.com/) for payment handling
- [x] Account with [Gmail](https://stripe.com/) for sending out email upon user registration

### To deploy on Heroku
1. Download the master branch from [github](https://github.com/jolenewai/flashing-stocks-app)
2. Alternatively, clone the master branch with the following command line in your IDE:
```
git clone https://github.com/jolenewai/flashing-stocks-app
```
2. To list all the requirements in requirements.txt, run the following command in terminal:
```
pip3 freeze --local > requirements.txt
```
3. Make sure to set Debug to False in settings.py
4. Create Procfile to register the app with the following line 
```
web: gunicorn flashing_stock_project.wsgi:application
```
5. Login to Heroku using the following command line :
```
heroku login
``` 
7. Git push to Heroku Master after all the documents are properly set up
6. In the Settings page of your Heroku app, set up the following Environment Variables with your own values:
- [x] UPLOADCARE_PUBLIC_KEY
- [x] UPLOADCARE_SECRET_KEY
- [x] STRIPE_PUBLISHABLE_KEY
- [x] STRIPE_SECRET_KEY
- [x] SIGING_SECRET
- [x] DATABASE_URL
- [x] EMAIL_HOST_USER
- [x] EMAIL_HOST_PASSWORD

## File Hierarchy and Organisation

Files are organised properly based on their functionality and purposes.
### static 
- __img__ - contains images required for the layout
- __js__ - contains javascript required for the front end 
- __css__ - contains css stylesheets required for the front end

### App Folders
__home__

Contains search function and landing page 

__photos__

Contains model, URLs, Views function for CRUD related to photos 

__photographers__

Contains model, URLs, Views function for CRUD related to photographers 

__customers__

Contains model, URLs, Views function for CRUD related to customers 

__site_admin__

Contains model, URLs, Views function for CRUD related to the site admin 

__cart__

Contains model, URLs, Views function for CRUD related to the Shopping Cart

__checkout__

Contains model, URLs, Views function for CRUD related to the Payment and Checkout

## Credits

### Content
- Terms of Use and License Agreements were modified from the [ShutterStock](https://www.shutterstock.com/)

### Media
- The photos used in this site were taken and edited by myself
- The screenshot is taken with [Am I Responsive](http://ami.responsivedesign.is/#)

### Acknowledgements
I received inspiration for this project from
- [ShutterStock](https://www.shutterstock.com/)
- [Pexels](https://www.pexels.com/)
