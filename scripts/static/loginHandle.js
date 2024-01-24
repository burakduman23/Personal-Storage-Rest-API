Vue.component("modal", {
    template: "#modal-template"
  });

  var app = new Vue({
    el: "#app",


    data: {
        serviceURL: "your url",
        authenticated: false,
        loggedIn: null,
        input: {
          username: "",
          password: ""
        }
      },
      methods: {
        login() {
          if (this.input.username != "" && this.input.password != "") {
            axios
            .post(this.serviceURL+"/login", {
                "username": this.input.username,
                "password": this.input.password
            })
            .then(response => {
                if (response.data.status == "success") {
                  this.authenticated = true;
                  this.loggedIn = response.data.user_id;
                  axios
                  .get(this.serviceURL+"/user");
                }
            })
            .catch(e => {
                alert("The username or password was incorrect, try again");
                this.input.password = "";
                console.log(e);
            });
          } else {
            alert("A username and password must be present");
          }
        }
    }
})