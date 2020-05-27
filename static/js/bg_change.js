$(function(){

    let bgImages = ["bg_image1.jpg", "bg_image2.jpg","bg_image3.jpg", "bg_image4.jpg", "bg_image5.jpg", "bg_image6.jpg","bg_image7.jpg", "bg_image8.jpg"]
    let img = new Image()
    let imgPath = 'images/'

    function preload(){

        for (let i of bgImages){
            img.url = imgPath+bgImages[i]
        }

        changeImage()
        setInterval(changeImage,8000)

    }
    function changeImage(){
        let randNum = Math.floor(Math.random() * 8)
        $('#home').css("background-image", "url(\'"+imgPath+bgImages[randNum]+"\')")   
    }

    preload()

})