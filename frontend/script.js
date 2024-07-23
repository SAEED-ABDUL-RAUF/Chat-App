
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


let plus_navigations_show = document.getElementById('plus_navigations_show');
let plus_navigations = document.getElementById('plus_navigations');

plus_navigations_show.addEventListener('click', () => {
  if (plus_navigations.style.display == 'none') {
    plus_navigations.style.display = 'block'
  } else {
    plus_navigations.style.display = 'none'
  }
})