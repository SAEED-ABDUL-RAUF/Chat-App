
//phone hamburger
let hamburger = document.getElementById('hamburger');
let navigations = document.getElementById('navigations');

hamburger.addEventListener('click', () => {
  if (navigations.style.top === '-224px') {
      navigations.style.transition = 'top 450ms ease';
      navigations.style.top = '35px';
  } else {
    navigations.style.transition = 'top 450ms ease';
    navigations.style.top = '-224px';
  }
})

// Defining a function to handle hiding the navigation
function hideNavigationIfVisible() {
  if (navigations.style.top === '35px') {
      navigations.style.transition = 'top 450ms ease';
      navigations.style.top = '-224px';
  }
}

//
let typeArea = document.getElementById('typeArea');
 onload = () => {
   let Message = document.getElementById('message');
  if (Message.value > 10) {
    typeArea.style.height = '70px';
  }
}
