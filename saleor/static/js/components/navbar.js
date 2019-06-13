const $toogleIcon = $('.navbar__brand__menu-toggle');
const $mobileNav = $('nav');
const $searchIcon = $('.mobile-search-icon');
const $closeSearchIcon = $('.mobile-close-search');
const $searchForm = $('.search-form');

const $flmToggle = $('a.nav-link');
const $flmUl = $('.nav-item__dropdown-content .container>ul');

const renderNavbar = () => {
  const $desktopLinkBar = $('.navbar__login');
  const $mobileLinkBar = $('.navbar__menu__login');
  const windowWidth = window.innerWidth;
  const $languagePicker = $('.language-picker');
  const $languagePickerButton = $('#language-picker-button');
  if (windowWidth < 768) {
    $flmUl.wrap('<div class="scroll-wrap"></div>');
  };

  if (windowWidth < 768) {
    const $desktopLinks = $desktopLinkBar.find('a').not('.dropdown-link');
    if ($desktopLinks.length) {
      $searchForm.addClass('search-form--hidden');
      $mobileNav.append('<ul class="nav navbar-nav navbar__menu__login"></ul>');
      $languagePicker.appendTo('.navbar__menu__login')
        .wrap('<li class="nav-item login-item"></li>')
        .addClass('nav-link');
      $desktopLinks
        .appendTo('.navbar__menu__login')
        .wrap('<li class="nav-item login-item"></li>')
        .addClass('nav-link');
      $desktopLinkBar
        .find('li')
        .remove();
    }
    $languagePickerButton.attr('data-target', '#languagePickerModal');
    $languagePickerButton.attr('data-toggle', 'modal');
  } else {
    const $mobileLinks = $mobileLinkBar.find('a').not('.dropdown-link');
    if ($mobileLinks.length) {
      $searchForm.removeClass('search-form--hidden');
      $languagePicker.appendTo('.navbar__login ul')
        .wrap('<li></li>')
        .removeClass('nav-link');
      $mobileLinks
        .appendTo('.navbar__login ul')
        .wrap('<li></li>')
        .removeClass('nav-link');
      $mobileLinkBar.remove();
    }
    $languagePickerButton.attr('data-target', '');
    $languagePickerButton.attr('data-toggle', 'dropdown');
  }
};

// -----

renderNavbar();
$toogleIcon
  .on('click', (e) => {
    $mobileNav.toggleClass('open');
    e.stopPropagation();
  });
$flmToggle
  .on('click', (e) => {
    $('.scroll-wrap').toggleClass('open');
    e.stopPropagation();
  });
$(document)
  .on('click', () => $mobileNav.removeClass('open'));
$(document)
  .on('click', () => $('.scroll-wrap').removeClass('open'));
$(window)
  .on('resize', renderNavbar);
$searchIcon
  .on('click', () => $searchForm.removeClass('search-form--hidden'));
$closeSearchIcon
  .on('click', () => $searchForm.addClass('search-form--hidden'));
