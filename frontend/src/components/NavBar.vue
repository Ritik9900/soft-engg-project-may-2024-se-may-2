<template>
    <nav class="navbar bg-body-tertiary">
      <div class="container-fluid">
        <div class="navbar-brand d-flex align-items-center">
          <img 
            :src="logoSrc" 
            :alt="logoAlt" 
            :width="logoWidth" 
            :height="logoHeight" 
            class="logo d-inline-block align-text-top"
          />
          <a href="/" class="brand-name">{{ brandName }}</a>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    data() {
      return {
        logoSrc: require('@/assets/iit_madras_logo.png'),
        logoAlt: "IIT Madras Logo",
        logoWidth: 50,
        logoHeight: 50,
        brandName: "IIT Madras"
      };
    }
  }
  </script>
  
  <style>
  .navbar {
    background-color: #ffffff;
    width: 100%;
    height: 60px;
    
  }
  
  .navbar-brand {
    display: flex;
    align-items: center;
    height: 100%;
  }
  
  .brand-name {
    font-size: 1.5rem; 
    margin-left: 15px; /* Space between logo and text */
    color: #000000; /* Ensure text color is not white */
    font-family: 'Poppins', sans-serif; /* Change to your desired font family */
    font-weight: bold; /* Make text bold */
    text-decoration: none; /* Remove underline */
    transition: transform 0.3s ease; 
  }
  
  .logo {
    transition: transform 0.3s ease; 
  }
  
  .brand-name:hover,
  .logo:hover {
    transform: scale(1.1); 
  }
  </style>
  