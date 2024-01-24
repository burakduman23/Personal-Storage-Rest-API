var app = new Vue({
    el: "#app",

    data: {
        serviceURL: "your url",
        authenticated: false,
        loggedIn: null,
        input: {
            firstname: "",
            lastname: "",
            email: "",
            username: "",
            password: ""
        }
    },

    methods: {
        register() {
            if (this.input.username != "" && this.input.password != "") {
                axios
                    .post(this.serviceURL + "/register", {
                        "firstName": this.input.firstname,
                        "lastName": this.input.lastname,
                        "email": this.input.email,
                        "username": this.input.username,
                        "password": this.input.password
                    })
                    .then(response => {
                        if (response.data.status == "success") {
                            this.authenticated = true;
                            this.loggedIn = response.data.user_id;
                            window.location.href = "/static/dashboard.html";
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