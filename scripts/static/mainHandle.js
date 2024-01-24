Vue.component("modal", {
    template: "#modal-template"
  });
var app = new Vue({
    el: "#app",

    data : {
        serviceURL: "your url",
        authenticated: false,
        loggedIn: null,

    },

    methods: {
        login(){
            window.location.href = "/static/loginPage.html";
        },
        register(){
            window.location.href = "/static/registerPage.html";
        }
    }
})