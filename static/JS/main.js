"use strict";const header=document.querySelector("header"),nav=document.querySelector("nav"),navbarMenuBtn=document.querySelector(".navbar-menu-btn"),navbarForm=document.querySelector(".navbar-form"),navbarFormCloseBtn=document.querySelector(".navbar-form-close"),navbarSearchBtn=document.querySelector(".navbar-search-btn");function navIsActive(){header.classList.toggle("active"),nav.classList.toggle("active"),navbarMenuBtn.classList.toggle("active")}navbarMenuBtn.addEventListener("click",navIsActive);const searchBarIsActive=()=>navbarForm.classList.toggle("active");navbarSearchBtn.addEventListener("click",searchBarIsActive),navbarFormCloseBtn.addEventListener("click",searchBarIsActive);